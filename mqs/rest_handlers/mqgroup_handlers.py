"""REST handlers for actions on MQ groups."""

import logging

from rest_tools.server import validate_request

from . import auth
from .base_handlers import BaseMQSHandler
from .. import config

LOGGER = logging.getLogger(__name__)


class MQGroupHandler(BaseMQSHandler):  # pylint: disable=W0223
    """The handler for creating MQ groups."""

    ROUTE = r"/mq-group$"

    @auth.service_account_auth(roles=auth.AuthAccounts.WMS)  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def post(self) -> None:
        """Handle POST requests."""


class MQGroupIDHandler(BaseMQSHandler):  # pylint: disable=W0223
    """The handler for interacting with MQ groups."""

    ROUTE = r"/mq-group/(?P<mqgroup_id>\w+)$"

    @auth.service_account_auth(roles=auth.AuthAccounts.WMS)  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self, mqgroup_id: str) -> None:
        """Handle GET requests."""
