"""Constants and tools for handling REST-requestor auth."""

import enum
import logging

import rest_tools
from rest_tools.server import token_attribute_role_mapping_auth

from ..config import ENV

LOGGER = logging.getLogger(__name__)


class AuthAccounts(enum.StrEnum):  # attrs are str subclass types! (no `.value` needed)
    """Accounts for auth."""

    USER = "user"
    WMS = "system-wms"


ALL_AUTH_ACCOUNTS = list(AuthAccounts.__members__.values())

if ENV.CI:

    def service_account_auth(**kwargs):  # type: ignore
        def make_wrapper(method):  # type: ignore[no-untyped-def]
            async def wrapper(self, *args, **kwargs):  # type: ignore[no-untyped-def]
                LOGGER.warning("TESTING: auth disabled")
                return await method(self, *args, **kwargs)

            return wrapper

        return make_wrapper

else:
    service_account_auth = token_attribute_role_mapping_auth(  # type: ignore[no-untyped-call]
        role_attrs={
            # AuthAccounts.USER: ["groups=/institutions/IceCube.*"],
            AuthAccounts.WMS: ["ewms_role=system-wms"],
        }
    )


def generate_queue_auth_token() -> str:
    """Generate auth token (JWT) for a queue."""
    if ENV.CI:
        return "TESTING-TOKEN"

    # TODO - put Auth instance in handler, then pass into this func
    return rest_tools.utils.Auth("mysecret").create_token("mysubject")
