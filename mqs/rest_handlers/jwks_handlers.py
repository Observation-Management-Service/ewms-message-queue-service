"""REST handlers for the JWKS endpoint."""

import json
import logging
import re

from jwt.algorithms import RSAAlgorithm
from rest_tools.server import validate_request

from . import rest_auth
from .base_handlers import BaseMQSHandler
from .. import config

LOGGER = logging.getLogger(__name__)


# ----------------------------------------------------------------------------


class JWKSJsonHandler(BaseMQSHandler):
    """Handles the JWKS JSON response."""

    ROUTE = re.escape("/.well-known/jwks.json") + "$"

    @rest_auth.service_account_auth(roles=rest_auth.ALL_AUTH_ACCOUNTS)  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self) -> None:
        """Handle GET."""
        key_obj = RSAAlgorithm(RSAAlgorithm.SHA256).prepare_key(
            key=config.ENV.BROKER_QUEUE_AUTH_PUBLIC_KEY
        )
        jwk = json.loads(RSAAlgorithm.to_jwk(key_obj))
        jwk["kid"] = "no-id"

        self.write(jwk)


# -----------------------------------------------------------------------------
