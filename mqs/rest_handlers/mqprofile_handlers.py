"""REST handlers for actions on MQ profiles."""

import logging

import tornado
from rest_tools.server import validate_request

from . import auth
from .base_handlers import BaseMQSHandler
from .. import config, utils
from ..database.client import DocumentNotFoundException

LOGGER = logging.getLogger(__name__)


class MQProfileIDHandler(BaseMQSHandler):  # pylint: disable=W0223
    """The handler for interacting with MQ profiles."""

    ROUTE = rf"/{config.ROUTE_VERSION_PREFIX}/mq-profiles/(?P<mqid>\w+)$"

    @auth.service_account_auth(roles=[auth.AuthAccounts.WMS])  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self, mqid: str) -> None:
        """Handle GET requests."""
        try:
            mqprofile = await self.mqprofile_client.find_one({"mqid": mqid})
        except DocumentNotFoundException:
            raise tornado.web.HTTPError(404, reason="MQProfile not found")

        self.write(mqprofile)


class MQProfilePublicGetHandler(BaseMQSHandler):  # pylint: disable=W0223
    """The handler for retrieving activated, public MQ profiles."""

    ROUTE = rf"/{config.ROUTE_VERSION_PREFIX}/workflows/(?P<workflow_id>\w+)/mq-profiles/public$"

    @auth.service_account_auth(roles=[auth.AuthAccounts.USER])  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self, workflow_id: str) -> None:
        """Handle GET requests."""

        mqprofiles = await utils.alist(
            self.mqprofile_client.find_all(
                {
                    "workflow_id": workflow_id,
                    "is_public": True,
                },
                projection=self.get_argument("projection", []),
            )
        )

        self.write({"mqprofiles": mqprofiles})
