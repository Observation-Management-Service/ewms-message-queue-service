"""Utilities for working with JWKS auth."""

import hashlib
import os
from pathlib import Path

from jwt.algorithms import RSAAlgorithm
from rest_tools.utils import Auth
from tornado import httputil

from mqs import config

BROKER_QUEUE_AUTH_ALGO = "RS256"


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

    @property
    def kid(self) -> str:
        return hashlib.sha512(self._public_key).hexdigest()

    def generate_jwt(self, request: httputil.HTTPServerRequest, mqid: str) -> str:
        """Generate auth token (JWT) for a queue."""
        if config.ENV.CI:
            return "TESTING-TOKEN"

        jwt_auth_handler = Auth(
            self.private_key,
            pub_secret=self.public_key,
            issuer=request.full_url().rstrip(request.uri),  # just the base url
            algorithm=BROKER_QUEUE_AUTH_ALGO,
        )

        return jwt_auth_handler.create_token(
            "mqs",
            expiration=config.ENV.BROKER_QUEUE_AUTH_TOKEN_EXP,
            payload={
                # https://www.rabbitmq.com/docs/oauth2#prerequisites
                # matches rabbitmq broker's 'resource_server_id' value
                "aud": config.ENV.BROKER_RESOURCE_SERVER_ID,
                # https://www.rabbitmq.com/docs/oauth2#rich-authorization-request
                "authorization_details": [
                    {
                        # https://www.rabbitmq.com/docs/oauth2#type-field
                        # -> matches rabbitmq broker's 'resource_server_type' value
                        "type": "rabbitmq",
                        # https://www.rabbitmq.com/docs/oauth2#locations-field
                        "locations": [
                            f"cluster:^{config.ENV.BROKER_RESOURCE_SERVER_ID}$/queue:^{mqid}$"
                        ],
                        # https://www.rabbitmq.com/docs/oauth2#actions-field
                        "actions": ["read", "write"],
                    }
                ],
            },
            headers={"kid": self.kid},
        )

    def get_jwks(self) -> list[dict[str, str]]:
        """Generate JWKS list."""
        key_obj = RSAAlgorithm(RSAAlgorithm.SHA256).prepare_key(key=self.public_key)
        jwk = RSAAlgorithm.to_jwk(key_obj, as_dict=True)
        jwk["kid"] = self.kid

        # TODO: add recently old jwks

        return [jwk]
