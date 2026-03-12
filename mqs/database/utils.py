"""utils.py."""

import logging
from urllib.parse import quote_plus

from pymongo import AsyncMongoClient

from ..config import ENV

LOGGER = logging.getLogger(__name__)

_DB_NAME = "MQS_DB"
MQPROFILE_COLL_NAME = "MQProfileColl"
MQGROUP_COLL_NAME = "MQGroupColl"

_JWKS_DB_NAME = "JWK_DB"
_JWKS_COLL_NAME = "JWKS_COLL"


async def create_mongodb_client() -> AsyncMongoClient:
    """Construct the MongoDB client."""
    auth_user = quote_plus(ENV.MONGODB_AUTH_USER)
    auth_pass = quote_plus(ENV.MONGODB_AUTH_PASS)

    if auth_user and auth_pass:
        url = f"mongodb://{auth_user}:{auth_pass}@{ENV.MONGODB_HOST}:{ENV.MONGODB_PORT}"
    else:
        url = f"mongodb://{ENV.MONGODB_HOST}:{ENV.MONGODB_PORT}"

    mongo_client = AsyncMongoClient(url)
    return mongo_client


def get_jwks_collection_obj(mongo_client: AsyncMongoClient):
    """Get the JWKS mongo collection object."""
    return mongo_client[_JWKS_DB_NAME][_JWKS_COLL_NAME]


async def ensure_indexes(mongo_client: AsyncMongoClient) -> None:
    """Create indexes in collections.

    Call on server startup.
    """
    LOGGER.info("Ensuring indexes...")

    async def make_index(db: str, coll: str, attr: str, unique: bool = False) -> None:
        LOGGER.info(f"creating index for ({db=}, {coll=}, {attr=}, {unique=})...")
        await mongo_client[db][coll].create_index(
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
