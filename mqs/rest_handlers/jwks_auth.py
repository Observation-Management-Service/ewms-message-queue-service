"""Utilities for working with JWKS auth."""

from urllib.parse import urljoin

from rest_tools.utils import Auth
from tornado import httputil

from .. import config


def generate_queue_jwt(request: httputil.HTTPServerRequest, mqid: str) -> str:
    """Generate auth token (JWT) for a queue."""
    if config.ENV.CI:
        return "TESTING-TOKEN"

    jwt_auth_handler = Auth(
        config.ENV.BROKER_QUEUE_AUTH_PRIVATE_KEY,
        pub_secret=config.ENV.BROKER_QUEUE_AUTH_PUBLIC_KEY,
        issuer=urljoin(  # mqs.my-url.aq/blah + /this = mqs.my-url.aq/this
            request.full_url(), "/.well-known/jwks.json"
        ),
        algorithm=config.BROKER_QUEUE_AUTH_ALGO,
    )

    return jwt_auth_handler.create_token(
        "mqs",
        expiration=config.ENV.BROKER_QUEUE_AUTH_TOKEN_EXP,
        payload={
            # https://www.rabbitmq.com/docs/oauth2#scope-translation
            # <permission>:<vhost_pattern>/<name_pattern>[/<routing_key_pattern>]
            "scope": f"write:*/{mqid}/*",
            # https://www.rabbitmq.com/docs/oauth2#prerequisites
            # matches rabbitmq broker's 'resource_server_id' value
            "aud": config.ENV.BROKER_RESOURCE_SERVER_ID,
        },
    )
