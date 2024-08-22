"""REST handlers for actions on MQ profiles."""

import logging

import tornado
from rest_tools.server import validate_request

from . import rest_auth
from .base_handlers import BaseMQSHandler
from .. import config, utils
from ..database.client import DocumentNotFoundException

LOGGER = logging.getLogger(__name__)


class MQProfileIDHandler(BaseMQSHandler):  # pylint: disable=W0223
    """The handler for interacting with MQ profiles."""

    ROUTE = rf"/{config.ROUTE_VERSION_PREFIX}/mqs/mq-profiles/(?P<mqid>[\w-]+)$"

    @rest_auth.service_account_auth(roles=[rest_auth.AuthAccounts.WMS])  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self, mqid: str) -> None:
        """Handle GET requests."""
        try:
            mqprofile = await self.mqprofile_client.find_one({"mqid": mqid})
        except DocumentNotFoundException:
            raise tornado.web.HTTPError(404, reason="MQProfile not found")

        self.write(mqprofile)


class MQProfilePublicGetHandler(BaseMQSHandler):  # pylint: disable=W0223
    """The handler for retrieving public MQ profiles."""

    ROUTE = rf"/{config.ROUTE_VERSION_PREFIX}/mqs/workflows/(?P<workflow_id>[\w-]+)/mq-profiles/public$"

    @rest_auth.service_account_auth(roles=[rest_auth.AuthAccounts.USER])  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self, workflow_id: str) -> None:
        """Handle GET requests."""

        mqprofiles = await utils.alist(
            self.mqprofile_client.find_all(
                {
                    "workflow_id": workflow_id,
                    "is_public": True,
                },
                projection=[],  # no great way to get a list from query params
            ),
        )

        self.write(
            {
                "mqprofiles": mqprofiles,
            }
        )
