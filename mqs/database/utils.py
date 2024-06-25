"""utils.py."""

import logging
from typing import Any
from urllib.parse import quote_plus

import jsonschema
from motor.motor_asyncio import AsyncIOMotorClient
from tornado import web

from ..config import ENV

LOGGER = logging.getLogger(__name__)

_DB_NAME = "MQS_DB"
MQPROFILE_COLL_NAME = "MQProfileColl"
MQGROUP_COLL_NAME = "MQGroupColl"

_JWKS_DB_NAME = "JWK_DB"
_JWKS_COLL_NAME = "JWKS_COLL"


def get_jsonschema_spec_name(collection_name: str) -> str:
    """Map between the two naming schemes."""
    return collection_name.removesuffix("Coll")


async def create_mongodb_client() -> AsyncIOMotorClient:  # type: ignore[valid-type]
    """Construct the MongoDB client."""
    auth_user = quote_plus(ENV.MONGODB_AUTH_USER)
    auth_pass = quote_plus(ENV.MONGODB_AUTH_PASS)

    if auth_user and auth_pass:
        url = f"mongodb://{auth_user}:{auth_pass}@{ENV.MONGODB_HOST}:{ENV.MONGODB_PORT}"
    else:
        url = f"mongodb://{ENV.MONGODB_HOST}:{ENV.MONGODB_PORT}"

    mongo_client = AsyncIOMotorClient(url)  # type: ignore[var-annotated]
    return mongo_client


def get_jwks_collection_obj(mongo_client: AsyncIOMotorClient):
    """Get the JWKS mongo collection object."""
    return mongo_client[_JWKS_DB_NAME][_JWKS_COLL_NAME]


async def ensure_indexes(mongo_client: AsyncIOMotorClient) -> None:  # type: ignore[valid-type]
    """Create indexes in collections.

    Call on server startup.
    """
    LOGGER.info("Ensuring indexes...")

    async def make_index(db: str, coll: str, attr: str, unique: bool = False) -> None:
        LOGGER.info(f"creating index for ({db=}, {coll=}, {attr=}, {unique=})...")
        await mongo_client[db][coll].create_index(  # type: ignore[index]
            attr,
            name=f"{attr.replace('.', '_')}_index",
            unique=unique,
            background=True,
        )

    # MQPROFILE
    await make_index(_DB_NAME, MQPROFILE_COLL_NAME, "mqid", unique=True)
    await make_index(_DB_NAME, MQPROFILE_COLL_NAME, "workflow_id")
    await make_index(_DB_NAME, MQPROFILE_COLL_NAME, "timestamp")

    # MQGROUP
    await make_index(_DB_NAME, MQGROUP_COLL_NAME, "workflow_id", unique=True)
    await make_index(_DB_NAME, MQGROUP_COLL_NAME, "timestamp")

    # JWKS
    await make_index(_JWKS_DB_NAME, _JWKS_COLL_NAME, "kid", unique=True)

    LOGGER.info("Ensured indexes (may continue in background).")


def web_jsonschema_validate(instance: Any, schema: dict) -> None:
    """Wrap `jsonschema.validate` with `web.HTTPError` (500)."""
    try:
        jsonschema.validate(instance, schema)
    except jsonschema.exceptions.ValidationError as e:
        LOGGER.exception(e)
        raise web.HTTPError(
            status_code=500,
            log_message=f"{e.__class__.__name__}: {e}",  # to stderr
            reason="Attempted to insert invalid data into database",  # to client
        )
