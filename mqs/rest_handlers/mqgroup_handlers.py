"""REST handlers for actions on MQ groups."""

import logging
import time

import mqclient
import tornado
from pymongo.errors import DuplicateKeyError
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

        # NOTE: this endpoint is idempotent -- make sure it stays that way

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
        try:
            async with await self.mqs_db.mongo_client.start_session() as s:
                async with s.start_transaction():  # atomic
                    mqgroup = await self.mqs_db.mqgroup_collection.insert_one(mqgroup)
                    mqprofiles = await self.mqs_db.mqprofile_collection.insert_many(
                        mqprofiles
                    )
        except DuplicateKeyError as e:
            if not (
                # criteria for this being caused by a duplicate 'workflow_id' value:
                e.details
                and "keyValue" in e.details
                and "workflow_id" in e.details["keyValue"].keys()
            ):
                raise e
            LOGGER.exception(e)
            LOGGER.warning(
                "Tried to reserve an existing MQ group (see exception above)"
                " -- retrieving existing docs from database..."
            )
            mqgroup = await self.mqs_db.mqgroup_collection.find_one(
                {"workflow_id": workflow_id}
            )
            mqprofiles = []
            async for x in self.mqs_db.mqprofile_collection.find_all(
                {"workflow_id": workflow_id}, projection=[]
            ):
                mqprofiles.append(x)

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
        #
        # NOTE: this endpoint is idempotent -- make sure it stays that way.
        #       the criteria may change on successive calls, which is okay

        mqid_auth_tokens = {}
        async for p in self.mqs_db.mqprofile_collection.find_all(
            {"workflow_id": workflow_id}, []
        ):
            mqid_auth_tokens[p["mqid"]] = await self.mqbroker_auth.generate_jwt(
                p["mqid"]
            )
        if not mqid_auth_tokens:
            raise tornado.web.HTTPError(
                404, reason="No MQProfiles found for workflow id"
            )

        # put all into db -- atomically
        async with await self.mqs_db.mongo_client.start_session() as s:
            async with s.start_transaction():  # atomic

                # update mqgroup
                try:
                    mqgroup = await self.mqs_db.mqgroup_collection.find_one_and_update(
                        {"workflow_id": workflow_id},
                        {
                            "$set": {
                                "criteria": criteria,
                            }
                        },
                    )
                except DocumentNotFoundException:
                    raise tornado.web.HTTPError(404, reason="MQGroup not found")

                # update each mqprofile
                mqprofiles = []
                for mqid, token in mqid_auth_tokens.items():
                    try:
                        mqp = await self.mqs_db.mqprofile_collection.find_one_and_update(
                            {"mqid": mqid},
                            {
                                "$set": {
                                    "is_activated": True,
                                    "auth_token": token,
                                    "broker_type": config.ENV.BROKER_TYPE,
                                    "broker_address": f"{config.ENV.BROKER_QUEUE_USERNAME}@{config.ENV.BROKER_URL}",
                                }
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
            mqgroup = await self.mqs_db.mqgroup_collection.find_one(
                {"workflow_id": workflow_id}
            )
        except DocumentNotFoundException:
            raise tornado.web.HTTPError(404, reason="MQGroup not found")

        self.write(mqgroup)
