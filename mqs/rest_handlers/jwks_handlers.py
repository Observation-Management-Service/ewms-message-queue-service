"""REST handlers for the JWKS endpoint."""

import logging

from rest_tools.server import validate_request

from . import rest_auth
from .base_handlers import BaseMQSHandler
from .. import config

LOGGER = logging.getLogger(__name__)


# ----------------------------------------------------------------------------


class WellKnownJWKSDotJSONHandler(BaseMQSHandler):
    """Handles the JWKS JSON response."""

    ROUTE = r"/.well-known/jwks.json$"

    @rest_auth.service_account_auth(roles=rest_auth.ALL_AUTH_ACCOUNTS)  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self) -> None:
        """Handle GET."""
        self.write(
            {
                "keys": await self.broker_queue_auth.get_jwks_from_db(),
            }
        )


# -----------------------------------------------------------------------------
