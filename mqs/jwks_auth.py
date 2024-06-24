"""Utilities for working with JWKS auth."""

import os
from pathlib import Path
from urllib.parse import urljoin

from rest_tools.utils import Auth
from tornado import httputil

from mqs import config


class BrokerQueueAuth:
    """Manages retrieving the public and private keys for the broker queue."""

    def __init__(self):
        self._public_key = None
        self._public_key_file_last_modtime = float("-inf")
        self._private_key = None
        self._private_key_file_last_modtime = float("-inf")

    @staticmethod
    def _retrieve_key(
        fpath: Path,
        fpath_last_modtime: float,
        current_val: bytes,
    ) -> tuple[float, bytes]:
        """Grab new key value from source file if it's been updated."""
        cur_mod = os.path.getmtime(fpath)
        if cur_mod > fpath_last_modtime:  # has file been updated since last time?
            with open(fpath, "rb") as f:
                return cur_mod, f.read()
        else:
            return fpath_last_modtime, current_val

    @property
    def public_key(self) -> bytes:
        """Public key, smartly cached so key source file can update on file system."""
        self._public_key_file_last_modtime, self._public_key = self._retrieve_key(
            config.ENV.BROKER_QUEUE_AUTH_PUBLIC_KEY_FILE,
            self._public_key_file_last_modtime,
            self._public_key,
        )
        return self._public_key

    @property
    def private_key(self) -> bytes:
        """Private key, smartly cached so key source file can update on file system."""
        self._private_key_file_last_modtime, self._private_key = self._retrieve_key(
            config.ENV.BROKER_QUEUE_AUTH_PRIVATE_KEY_FILE,
            self._private_key_file_last_modtime,
            self._private_key,
        )
        return self._private_key

    def generate_jwt(self, request: httputil.HTTPServerRequest, mqid: str) -> str:
        """Generate auth token (JWT) for a queue."""
        if config.ENV.CI:
            return "TESTING-TOKEN"

        jwt_auth_handler = Auth(
            self.private_key,
            pub_secret=self.public_key,
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
