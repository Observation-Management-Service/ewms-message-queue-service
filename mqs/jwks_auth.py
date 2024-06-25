"""Utilities for working with JWKS auth."""

import hashlib
import os
from pathlib import Path

import motor.motor_asyncio
from jwt.algorithms import RSAAlgorithm
from rest_tools.utils import Auth
from tornado import httputil

from . import config

BROKER_QUEUE_AUTH_ALGO = "RS256"


class BrokerQueueAuth:
    """Manages retrieving the public and private keys for the broker queue."""

    def __init__(
        self,
        mongo_client: motor.motor_asyncio.AsyncIOMotorClient,
    ):
        self._mongo_collection = mongo_client["JWK_DB"]["JWKS"]
        self._pub_key = b""
        self._pub_key_file_last_modtime = float("-inf")
        self._priv_key = b""
        self._priv_key_file_last_modtime = float("-inf")

        self.kid = ""

    @staticmethod
    def _retrieve_key(
        fpath: Path,
        fpath_last_modtime: float,
        current_val: bytes,
    ) -> tuple[float, bytes, bool]:
        """Grab new key value from source file if it's been updated."""
        cur_mod = os.path.getmtime(fpath)
        if cur_mod > fpath_last_modtime:  # has file been updated since last time?
            with open(fpath, "rb") as f:
                return cur_mod, f.read(), True
        else:
            return fpath_last_modtime, current_val, False

    async def get_public_key(self) -> bytes:
        """Public key, smartly cached so key source file can update on file system."""
        self._pub_key_file_last_modtime, self._pub_key, updated = self._retrieve_key(
            config.ENV.BROKER_QUEUE_AUTH_PUBLIC_KEY_FILE,
            self._pub_key_file_last_modtime,
            self._pub_key,
        )
        if updated:
            await self._update_jwks_in_db()
            self.kid = hashlib.sha512(self._pub_key).hexdigest()
        return self._pub_key

    @property
    def private_key(self) -> bytes:
        """Private key, smartly cached so key source file can update on file system."""
        self._priv_key_file_last_modtime, self._priv_key, _ = self._retrieve_key(
            config.ENV.BROKER_QUEUE_AUTH_PRIVATE_KEY_FILE,
            self._priv_key_file_last_modtime,
            self._priv_key,
        )
        # don't store this in db
        return self._priv_key

    def generate_jwt(self, request: httputil.HTTPServerRequest, mqid: str) -> str:
        """Generate auth token (JWT) for a queue."""
        if config.ENV.CI:
            return "TESTING-TOKEN"

        jwt_auth_handler = Auth(
            self.private_key,
            pub_secret=self.get_public_key,
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

    async def _update_jwks_in_db(self) -> None:
        """Add a JWK to the database and remove old ones.

        Triggered when a public key is updated.
        """
        if await self._mongo_collection.find_one({"kid": self.kid}):
            return

        # make new jwk
        key_obj = RSAAlgorithm(RSAAlgorithm.SHA256).prepare_key(
            key=await self.get_public_key()
        )
        jwk = RSAAlgorithm.to_jwk(key_obj, as_dict=True)
        jwk["kid"] = self.kid

        # put in db
        await self._mongo_collection.insert_one(jwk)

        # TODO: remove any expired

    async def get_jwks_from_db(self) -> list[dict[str, str]]:
        """Retrieve the JWKS list from the database."""
        return [d async for d in self._mongo_collection.find()]
