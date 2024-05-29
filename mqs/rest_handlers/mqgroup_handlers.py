"""REST handlers for actions on MQ groups."""

import logging
import time

import mqclient
import tornado
from rest_tools.server import validate_request

from . import auth
from .base_handlers import BaseMQSHandler
from .. import config
from ..database.client import DocumentNotFoundException

LOGGER = logging.getLogger(__name__)


class MQGroupReservationHandler(BaseMQSHandler):  # pylint: disable=W0223
    """The handler for reserving MQ groups."""

    ROUTE = rf"/{config.ROUTE_VERSION_PREFIX}/workflows/(?P<workflow_id>\w+)/mq-group/reservation$"

    @auth.service_account_auth(roles=[auth.AuthAccounts.WMS])  # type: ignore
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
                "mqid": mqclient.Queue.make_name(),
                "workflow_id": workflow_id,
                "timestamp": now,
                "alias": alias,
                "is_public": bool(alias in self.get_argument("public")),
                "is_activated": False,
            }
            for alias in self.get_argument("queue_aliases")
        ]

        # put in db -- do last in case any exceptions above
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

    ROUTE = rf"/{config.ROUTE_VERSION_PREFIX}/workflows/(?P<workflow_id>\w+)/mq-group/activation$"

    @auth.service_account_auth(roles=[auth.AuthAccounts.WMS])  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def post(self, workflow_id: str) -> None:
        """Handle POST requests."""
        criteria: dict[str, int] = self.get_argument("criteria")

        # TODO: use criteria to determine if group can be activated

        # update db
        mqgroup = await self.mqgroup_client.find_one_and_update(
            {"workflow_id": workflow_id},
            {"criteria": criteria},
        )
        mqprofiles = await self.mqprofile_client.update_set_many(
            {"workflow_id": workflow_id},
            {"is_activated": True},
        )

        self.write(
            {
                "mqgroup": mqgroup,
                "mqprofiles": mqprofiles,
            }
        )


class MQGroupGetHandler(BaseMQSHandler):  # pylint: disable=W0223
    """The handler for interacting with MQ groups."""

    ROUTE = rf"/{config.ROUTE_VERSION_PREFIX}/workflows/(?P<workflow_id>\w+)/mq-group$"

    @auth.service_account_auth(roles=[auth.AuthAccounts.WMS])  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self, workflow_id: str) -> None:
        """Handle GET requests."""
        try:
            mqgroup = await self.mqgroup_client.find_one({"workflow_id": workflow_id})
        except DocumentNotFoundException:
            raise tornado.web.HTTPError(404, reason="MQGroup not found")

        self.write(mqgroup)
