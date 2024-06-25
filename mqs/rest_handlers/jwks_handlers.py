"""REST handlers for the JWKS endpoint."""

import logging
import re

from rest_tools.server import validate_request

from .. import config
from . import rest_auth
from .base_handlers import BaseMQSHandler

LOGGER = logging.getLogger(__name__)


# ----------------------------------------------------------------------------


class JWKSJsonHandler(BaseMQSHandler):
    """Handles the JWKS JSON response."""

    ROUTE = re.escape("/.well-known/jwks.json") + "$"

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
