"""Base REST handlers for the MQS REST API server interface."""

import logging
from typing import Any

from pymongo import AsyncMongoClient
from rest_tools.server import RestHandler, validate_request

from . import rest_auth
from .. import config, database
from ..jwks_auth import BrokerQueueAuth

LOGGER = logging.getLogger(__name__)


class BaseMQSHandler(RestHandler):  # pylint: disable=W0223
    """BaseMQSHandler is a RestHandler for all MQS routes."""

    def initialize(  # type: ignore[override]
        self,
        mongo_client: AsyncMongoClient,
        mqbroker_auth: BrokerQueueAuth,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize a BaseMQSHandler object."""
        super().initialize(*args, **kwargs)
        # pylint: disable=W0201
        self.mqs_db = database.client.MQSMongoValidatedDatabase(mongo_client)
        self.mqbroker_auth = mqbroker_auth


# ----------------------------------------------------------------------------


class MainHandler(BaseMQSHandler):  # pylint: disable=W0223
    """MainHandler is a BaseMQSHandler that handles the root route."""

    ROUTE = rf"/{config.URL_V_PREFIX}/mqs$"

    @rest_auth.service_account_auth(roles=rest_auth.ALL_AUTH_ACCOUNTS)  # type: ignore
    @validate_request(config.OPENAPI_SPEC)
    async def get(self) -> None:
        """Handle GET."""
        self.write({})


# -----------------------------------------------------------------------------

# ALL OTHER HANDLERS GO IN DEDICATED MODULES
