"""REST handlers for grabbing JSON-schema for any route."""

import logging

from rest_tools.server import validate_request

from . import rest_auth
from .base_handlers import BaseMQSHandler
from .. import config

LOGGER = logging.getLogger(__name__)


class SchemaHandler(BaseMQSHandler):  # pylint: disable=W0223
    """The sole handler for retrieving the OpenAPI schema."""

    ROUTE = rf"/{config.URL_V_PREFIX}/mqs/schema/openapi$"

    @rest_auth.service_account_auth(roles=rest_auth.ALL_AUTH_ACCOUNTS)  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self) -> None:
        """Handle GET."""
        # get the underlying dict (json)
        self.write(  # NOTE - if this doesn't work then use accessor.open ctx-mgr
            config.REST_OPENAPI_SPEC.spec.accessor.lookup,  # type: ignore[attr-defined]
        )
