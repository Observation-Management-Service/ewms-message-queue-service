"""REST handlers for actions on MQ profiles."""

import logging

import tornado
from rest_tools.server import validate_request

from . import auth
from .base_handlers import BaseMQSHandler
from .. import config
from ..database.client import DocumentNotFoundException

LOGGER = logging.getLogger(__name__)


class MQProfileIDHandler(BaseMQSHandler):  # pylint: disable=W0223
    """The handler for interacting with MQ profiles."""

    ROUTE = r"/mq/(?P<mqid>\w+)$"

    @auth.service_account_auth(roles=auth.AuthAccounts.WMS)  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self, mqid: str) -> None:
        """Handle GET requests."""
        try:
            mqprofile = await self.mqprofile_client.find_one(dict(mqid=mqid))
        except DocumentNotFoundException:
            raise tornado.web.HTTPError(404, reason="MQProfile not found")

        self.write(mqprofile)
