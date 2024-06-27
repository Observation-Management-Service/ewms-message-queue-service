"""Utilities for working with JWKS auth."""

import hashlib
import logging
import os
import time
import urllib.parse
from pathlib import Path

import motor.motor_asyncio
from jwt.algorithms import RSAAlgorithm
from rest_tools.utils import Auth

from . import config
from .database.utils import get_jwks_collection_obj

LOGGER = logging.getLogger(__name__)


# -----------------------------------------------------------------------------


BROKER_QUEUE_AUTH_ALGO = "RS256"

BROKER_QUEUE_AUTH_PATH_COMPONENT = "mqbroker-issuer"
BROKER_QUEUE_AUTH_ISSUER_URL = urllib.parse.urljoin(
    config.ENV.HERE_URL, BROKER_QUEUE_AUTH_PATH_COMPONENT
)


# -----------------------------------------------------------------------------


class BrokerQueueAuth:
    """Manages retrieving the public and private keys for the broker queue."""

    def __init__(
        self,
        mongo_client: motor.motor_asyncio.AsyncIOMotorClient,
    ):
        self._mongo_collection = get_jwks_collection_obj(mongo_client)
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
            LOGGER.info("Updated broker-queue auth public key")
            await self._update_jwks_in_db()
            self.kid = hashlib.sha512(self._pub_key).hexdigest()
        return self._pub_key

    @property
    def private_key(self) -> bytes:
        """Private key, smartly cached so key source file can update on file system."""
        self._priv_key_file_last_modtime, self._priv_key, updated = self._retrieve_key(
            config.ENV.BROKER_QUEUE_AUTH_PRIVATE_KEY_FILE,
            self._priv_key_file_last_modtime,
            self._priv_key,
        )
        if updated:
            LOGGER.info("Updated broker-queue auth private key")
        # don't store this in db
        return self._priv_key

    def generate_jwt(self, mqid: str) -> str:
        """Generate auth token (JWT) for a queue."""
        if config.ENV.CI:
            return "TESTING-TOKEN"

        jwt_auth_handler = Auth(
            self.private_key,
            pub_secret=self.get_public_key(),
            # don't auto-detect url in case k8s ingress is redirecting the incoming request
            # -> aka, k8s is 'using spec.rules.http.path' prefix
            issuer=BROKER_QUEUE_AUTH_ISSUER_URL,
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
        # check if this was actually an update; else, the process just restarted
        if await self._mongo_collection.find_one({"kid": self.kid}):
            LOGGER.info("Updated broker-queue auth public key is already in db")
            return

        # set exp on "current" jwk
        await self._mongo_collection.update_many(  # expected to be only 1 doc
            {
                "_exp": float("inf"),  # get those w/ field that is unset
            },
            {
                # set exp so it is greater than the last jwt generated using jwk's pub key
                "$set": {"_exp": time.time() + config.ENV.BROKER_QUEUE_AUTH_TOKEN_EXP},
            },
        )
        LOGGER.info("Set expiration for previous JWK in db")

        # insert new jwk
        key_obj = RSAAlgorithm(RSAAlgorithm.SHA256).prepare_key(
            key=await self.get_public_key()
        )
        jwk = {
            "kid": self.kid,
            "_exp": float("inf"),
            **RSAAlgorithm.to_jwk(key_obj, as_dict=True),
        }
        await self._mongo_collection.insert_one(jwk)
        LOGGER.info("Added new JWK to db")

    async def get_jwks_from_db(self) -> list[dict[str, str]]:
        """Retrieve the JWKS list from the database."""
        # remove any expired
        res = await self._mongo_collection.delete_many({"_exp": {"$lt": time.time()}})
        LOGGER.info(f"Deleted {res.deleted_count} expired JWKs")

        # get all
        jwks = [d async for d in self._mongo_collection.find()]
        LOGGER.info(f"Retrieved all ({len(jwks)}) JWKS dicts")

        return jwks
