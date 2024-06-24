"""REST handlers for ."""

import logging
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient
from rest_tools.server import RestHandler
from rest_tools.server import validate_request

from . import auth
from .. import config
from .. import database as db

LOGGER = logging.getLogger(__name__)


class BaseMQSHandler(RestHandler):  # pylint: disable=W0223
    """BaseMQSHandler is a RestHandler for all MQS routes."""

    def initialize(  # type: ignore  # pylint: disable=W0221
        self,
        mongo_client: AsyncIOMotorClient,  # type: ignore[valid-type]
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


# ----------------------------------------------------------------------------


class MainHandler(BaseMQSHandler):  # pylint: disable=W0223
    """MainHandler is a BaseMQSHandler that handles the root route."""

    ROUTE = rf"/{config.ROUTE_VERSION_PREFIX}/mqs$"

    @auth.service_account_auth(roles=[auth.ALL_AUTH_ACCOUNTS])  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self) -> None:
        """Handle GET."""
        self.write({})


# -----------------------------------------------------------------------------

# ALL OTHER HANDLERS GO IN DEDICATED MODULES
