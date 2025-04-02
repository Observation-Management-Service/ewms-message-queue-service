"""REST handlers for actions on MQ groups."""

import logging
import time

import mqclient
import tornado
from rest_tools.server import validate_request

from . import rest_auth
from .base_handlers import BaseMQSHandler
from .. import config
from ..database.client import DocumentNotFoundException

LOGGER = logging.getLogger(__name__)


class MQGroupReservationHandler(BaseMQSHandler):  # pylint: disable=W0223
    """The handler for reserving MQ groups."""

    ROUTE = rf"/{config.URL_V_PREFIX}/mqs/workflows/(?P<workflow_id>[\w-]+)/mq-group/reservation$"

    @rest_auth.service_account_auth(roles=[rest_auth.AuthAccounts.WMS])  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def post(self, workflow_id: str) -> None:
        """Handle POST requests."""
        now = time.time()

        # insert mq group
        mqgroup = {
            "workflow_id": workflow_id,
            "timestamp": now,
            "criteria": None,  # updated by /workflows/<workflow_id>/mq-group/activation
        }

        # insert mq profiles
        mqprofiles = [
            {
                # static/constant:
                "mqid": mqclient.Queue.make_name(),
                "workflow_id": workflow_id,
                "timestamp": now,
                "alias": alias,
                "is_public": bool(alias in self.get_argument("public")),
                "is_activated": False,
                #
                # to be added upon activation:
                "auth_token": None,
                "broker_type": None,
                "broker_address": None,
            }
            for alias in self.get_argument("queue_aliases")
        ]

        # put in db -- do last in case any exceptions above
        async with await self.mqgroup_client.mongo_client.start_session() as s:
            async with s.start_transaction():  # atomic
                mqgroup = await self.mqgroup_client.insert_one(mqgroup)
                mqprofiles = await self.mqprofile_client.insert_many(mqprofiles)

        self.write(
            {
                "mqgroup": mqgroup,
                "mqprofiles": mqprofiles,
            }
        )


class MQGroupActivationHandler(BaseMQSHandler):  # pylint: disable=W0223
    """The handler for activating MQ groups."""

    ROUTE = rf"/{config.URL_V_PREFIX}/mqs/workflows/(?P<workflow_id>[\w-]+)/mq-group/activation$"

    @rest_auth.service_account_auth(roles=[rest_auth.AuthAccounts.WMS])  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def post(self, workflow_id: str) -> None:
        """Handle POST requests."""
        criteria: dict[str, int] = self.get_argument("criteria")

        # TODO: use criteria to determine if group can be activated

        mqid_auth_tokens = {}
        async for p in self.mqprofile_client.find_all({"workflow_id": workflow_id}, []):
            mqid_auth_tokens[p["mqid"]] = await self.mqbroker_auth.generate_jwt(
                p["mqid"]
            )
        if not mqid_auth_tokens:
            raise tornado.web.HTTPError(
                404, reason="No MQProfiles found for workflow id"
            )

        # put all into db -- atomically
        async with await self.mqgroup_client.mongo_client.start_session() as s:
            async with s.start_transaction():  # atomic

                # update mqgroup
                try:
                    mqgroup = await self.mqgroup_client.find_one_and_update(
                        {"workflow_id": workflow_id},
                        {"criteria": criteria},
                    )
                except DocumentNotFoundException:
                    raise tornado.web.HTTPError(404, reason="MQGroup not found")

                # update each mqprofile
                mqprofiles = []
                for mqid, token in mqid_auth_tokens.items():
                    try:
                        mqp = await self.mqprofile_client.find_one_and_update(
                            {"mqid": mqid},
                            {
                                "is_activated": True,
                                "auth_token": token,
                                "broker_type": config.ENV.BROKER_TYPE,
                                "broker_address": f"{config.ENV.BROKER_QUEUE_USERNAME}@{config.ENV.BROKER_URL}",
                            },
                        )
                    except DocumentNotFoundException:
                        raise tornado.web.HTTPError(404, reason="MQProfile not found")
                    mqprofiles.append(mqp)

        self.write(
            {
                "mqgroup": mqgroup,
                "mqprofiles": mqprofiles,
            }
        )


class MQGroupGetHandler(BaseMQSHandler):  # pylint: disable=W0223
    """The handler for interacting with MQ groups."""

    ROUTE = rf"/{config.URL_V_PREFIX}/mqs/workflows/(?P<workflow_id>[\w-]+)/mq-group$"

    @rest_auth.service_account_auth(roles=[rest_auth.AuthAccounts.WMS])  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self, workflow_id: str) -> None:
        """Handle GET requests."""
        try:
            mqgroup = await self.mqgroup_client.find_one({"workflow_id": workflow_id})
        except DocumentNotFoundException:
            raise tornado.web.HTTPError(404, reason="MQGroup not found")

        self.write(mqgroup)
