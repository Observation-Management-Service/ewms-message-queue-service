"""REST handlers for the JWKS endpoint."""

import logging
import re

from rest_tools.server import validate_request

from .base_handlers import BaseMQSHandler
from .. import config
from ..jwks_auth import BROKER_QUEUE_AUTH_PATH_COMPONENT

LOGGER = logging.getLogger(__name__)


# ----------------------------------------------------------------------------


class WellKnownJWKSDotJSONHandler(BaseMQSHandler):
    """Handles the JWKS JSON response."""

    ROUTE = (
        re.escape(f"/{BROKER_QUEUE_AUTH_PATH_COMPONENT}/.well-known/jwks.json") + "$"
    )

    # public endpoint
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self) -> None:
        """Handle GET."""
        self.write(
            {
                "keys": await self.mqbroker_auth.get_jwks_from_db(),
            }
        )


# -----------------------------------------------------------------------------
