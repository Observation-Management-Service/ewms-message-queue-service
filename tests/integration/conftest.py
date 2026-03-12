"""conftest.py."""

import logging
import os
from collections.abc import AsyncIterator
from typing import cast

import pytest_asyncio
from pymongo import MongoClient
from rest_tools.client import RestClient
from wipac_dev_tools import logging_tools
from wipac_dev_tools.logging_tools import LoggerLevel

from .utils import refresh_mqbroker_key_files

LOGGER = logging.getLogger(__name__)


logging_tools.set_level(
    cast(LoggerLevel, os.getenv("LOG_LEVEL", "DEBUG")),
    first_party_loggers=["mqs"],
    third_party_level=cast(LoggerLevel, os.getenv("LOG_LEVEL_THIRD_PARTY", "INFO")),
    future_third_parties=[],
    specialty_loggers={
        "wipac-telemetry": "WARNING",
        "parse": "INFO",  # from openapi
        "rest_tools": cast(LoggerLevel, os.getenv("LOG_LEVEL_REST_TOOLS", "DEBUG")),
    },
)


@pytest_asyncio.fixture
async def rc() -> AsyncIterator[RestClient]:
    """Yield a RestClient."""
    mongo_client = MongoClient(  # type: ignore[var-annotated]
        f"mongodb://{os.environ['MONGODB_HOST']}:{os.environ['MONGODB_PORT']}"
    )

    # make sure custom dbs' collections are empty
    for db in mongo_client.list_database_names():
        if db not in ["admin", "config", "local"]:
            for coll in mongo_client[db].list_collection_names():
                mongo_client[db][coll].delete_many({})

    # write public and private files
    refresh_mqbroker_key_files()

    # connect rc
    yield RestClient(
        f'http://{os.environ["REST_HOST"]}:{os.environ["REST_PORT"]}',
        timeout=3,
        retries=2,
    )
