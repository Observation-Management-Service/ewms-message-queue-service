"""Root python script for MQS REST API server interface."""

import logging
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient
from rest_tools.server import RestHandlerSetup, RestServer

from . import rest_handlers
from .config import ENV
from .jwks_auth import BrokerQueueAuth

LOGGER = logging.getLogger(__name__)

HANDLERS = [
    rest_handlers.base_handlers.MainHandler,
    #
    rest_handlers.schema_handlers.SchemaHandler,
    #
    rest_handlers.mqgroup_handlers.MQGroupReservationHandler,
    rest_handlers.mqgroup_handlers.MQGroupActivationHandler,
    rest_handlers.mqgroup_handlers.MQGroupGetHandler,
    #
    rest_handlers.mqprofile_handlers.MQProfileIDHandler,
    rest_handlers.mqprofile_handlers.MQProfilePublicGetHandler,
    #
    rest_handlers.jwks_handlers.WellKnownJWKSDotJSONHandler,
]


async def make(mongo_client: AsyncIOMotorClient) -> RestServer:  # type: ignore[valid-type]
    """Make a MQS REST service (does not start up automatically)."""
    rhs_config: dict[str, Any] = {"debug": ENV.CI}
    if ENV.AUTH_OPENID_URL:
        rhs_config["auth"] = {
            "audience": ENV.AUTH_AUDIENCE,
            "openid_url": ENV.AUTH_OPENID_URL,
        }
    args = RestHandlerSetup(rhs_config)

    #
    # Setup clients/apis
    args["mongo_client"] = mongo_client
    args["broker_queue_auth"] = BrokerQueueAuth(mongo_client)

    # Configure REST Routes
    rs = RestServer(debug=ENV.CI)

    for klass in HANDLERS:
        # register route handler
        route = getattr(klass, "ROUTE")  # -> AttributeError
        rs.add_route(route, klass, args)
        LOGGER.info(f"Added handler: {klass.__name__}")

    return rs
