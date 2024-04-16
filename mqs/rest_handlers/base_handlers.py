"""Base REST handlers for the MQS REST API server interface."""

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
        self.task_directives_client = db.client.MQSMongoClient(
            mongo_client,
            db.utils.TASK_DIRECTIVES_COLL_NAME,
        )
        self.taskforces_client = db.client.MQSMongoClient(
            mongo_client,
            db.utils.TASKFORCES_COLL_NAME,
        )


# ----------------------------------------------------------------------------


class MainHandler(BaseMQSHandler):  # pylint: disable=W0223
    """MainHandler is a BaseMQSHandler that handles the root route."""

    ROUTE = r"/$"

    @auth.service_account_auth(roles=[auth.AuthAccounts.USER])  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self) -> None:
        """Handle GET."""
        self.write({})

# -----------------------------------------------------------------------------

# ALL OTHER HANDLERS GO IN DEDICATED MODULES
