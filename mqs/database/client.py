"""Tools for interacting with the mongo database."""

import logging

import jsonschema
from motor.motor_asyncio import AsyncIOMotorClient
from tornado import web
from wipac_dev_tools.mongo_jsonschema_tools import (
    IllegalDotsNotationActionException,
    MongoJSONSchemaValidatedCollection,
)

from .utils import (
    MQGROUP_COLL_NAME,
    MQPROFILE_COLL_NAME,
    _DB_NAME,
    get_jsonschema_spec_name,
)
from ..config import MONGO_COLLECTION_JSONSCHEMA_SPECS

__all__ = [  # export
    "DocumentNotFoundException",
]


def _validation_exception_callback(exc: Exception) -> Exception:
    """Translate exceptions for web use."""
    match exc:
        case jsonschema.exceptions.ValidationError():
            return web.HTTPError(
                status_code=500,
                log_message=f"{exc.__class__.__name__}: {exc}",  # to stderr
                reason="Attempted to insert invalid data into database",  # to client
            )
        case IllegalDotsNotationActionException():
            return web.HTTPError(
                status_code=500,
                log_message=f"{exc.__class__.__name__}: {exc}",  # to stderr
                reason="Could not perform action on database with provided syntax",  # to client
            )
        case _:
            return exc


class MQSMongoValidatedDatabase:
    """Wraps a MongoDB client and collection clients with json schema validation."""

    def __init__(
        self,
        mongo_client: AsyncIOMotorClient,
        parent_logger: logging.Logger | None = None,
    ):
        self.mongo_client = mongo_client
        self.mqprofile_collection = MongoJSONSchemaValidatedCollection(
            mongo_client[_DB_NAME][MQPROFILE_COLL_NAME],
            MONGO_COLLECTION_JSONSCHEMA_SPECS[
                get_jsonschema_spec_name(MQPROFILE_COLL_NAME)
            ],
            parent_logger,
            validation_exception_callback=_validation_exception_callback,
        )
        self.mqgroup_collection = MongoJSONSchemaValidatedCollection(
            mongo_client[_DB_NAME][MQGROUP_COLL_NAME],
            MONGO_COLLECTION_JSONSCHEMA_SPECS[
                get_jsonschema_spec_name(MQGROUP_COLL_NAME)
            ],
            parent_logger,
            validation_exception_callback=_validation_exception_callback,
        )
