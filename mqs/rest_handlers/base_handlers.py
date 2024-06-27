"""Base REST handlers for the MQS REST API server interface."""

import logging
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient
from rest_tools.server import RestHandler, validate_request

from . import rest_auth
from .. import config, database as db
from ..jwks_auth import BrokerQueueAuth

LOGGER = logging.getLogger(__name__)


class BaseMQSHandler(RestHandler):  # pylint: disable=W0223
    """BaseMQSHandler is a RestHandler for all MQS routes."""

    def initialize(  # type: ignore  # pylint: disable=W0221
        self,
        mongo_client: AsyncIOMotorClient,  # type: ignore[valid-type]
        mqbroker_auth: BrokerQueueAuth,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize a BaseMQSHandler object."""
        super().initialize(*args, **kwargs)  # type: ignore[no-untyped-call]
        # pylint: disable=W0201
        self.mqprofile_client = db.client.JSONSchemaMongoClient(
            mongo_client,
            db.utils.MQPROFILE_COLL_NAME,
        )
        self.mqgroup_client = db.client.JSONSchemaMongoClient(
            mongo_client,
            db.utils.MQGROUP_COLL_NAME,
        )
        self.mqbroker_auth = mqbroker_auth


# ----------------------------------------------------------------------------


class MainHandler(BaseMQSHandler):  # pylint: disable=W0223
    """MainHandler is a BaseMQSHandler that handles the root route."""

    ROUTE = rf"/{config.ROUTE_VERSION_PREFIX}/mqs$"

    @rest_auth.service_account_auth(roles=rest_auth.ALL_AUTH_ACCOUNTS)  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self) -> None:
        """Handle GET."""
        self.write({})


# -----------------------------------------------------------------------------

# ALL OTHER HANDLERS GO IN DEDICATED MODULES
