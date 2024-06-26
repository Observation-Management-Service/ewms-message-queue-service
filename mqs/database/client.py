"""Tools for interacting with the mongo database."""

import copy
import logging
from typing import Any, AsyncIterator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import ReturnDocument

from .utils import _DB_NAME, get_jsonschema_spec_name, web_jsonschema_validate
from ..config import MONGO_COLLECTION_JSONSCHEMA_SPECS


class DocumentNotFoundException(Exception):
    """Raised when document is not found for a particular query."""


class JSONSchemaMongoClient:
    """A generic client for interacting with mongo collections with jsonschema validation."""

    def __init__(
        self,
        mongo_client: AsyncIOMotorClient,  # type: ignore[valid-type]
        collection_name: str,
    ) -> None:
        self.mongo_client = mongo_client
        self._collection: AsyncIOMotorCollection = AsyncIOMotorCollection(
            mongo_client[_DB_NAME],  # type: ignore[arg-type]
            collection_name,
        )
        self._schema = MONGO_COLLECTION_JSONSCHEMA_SPECS[
            get_jsonschema_spec_name(collection_name)
        ]

        # like schema, but for partial updates
        self._schema_partial = copy.deepcopy(self._schema)
        self._schema_partial["required"] = []

        self.logger = logging.getLogger(f"{__name__}.{collection_name.lower()}")

    ####################################################################
    # WRITES
    ####################################################################

    async def insert_one(self, doc: dict) -> dict:
        """Insert the doc (dict)."""
        self.logger.debug(f"inserting one: {doc}")

        web_jsonschema_validate(doc, self._schema)
        await self._collection.insert_one(doc)
        # https://pymongo.readthedocs.io/en/stable/faq.html#writes-and-ids
        doc.pop("_id")

        self.logger.debug(f"inserted one: {doc}")
        return doc

    async def insert_many(self, docs: list[dict]) -> list[dict]:
        """Insert the docs (dicts)."""
        self.logger.debug(f"inserting many: {docs}")

        for doc in docs:
            web_jsonschema_validate(doc, self._schema)

        await self._collection.insert_many(docs)
        # https://pymongo.readthedocs.io/en/stable/faq.html#writes-and-ids
        for doc in docs:
            doc.pop("_id")

        self.logger.debug(f"inserted many: {docs}")
        return docs

    async def find_one_and_update(
        self,
        query: dict,
        set_update: dict,
        **kwargs: Any,
    ) -> dict:
        """Update the doc and return updated doc."""
        self.logger.debug(f"update one with query: {query}")

        web_jsonschema_validate(set_update, self._schema_partial)
        doc = await self._collection.find_one_and_update(
            query,
            {"$set": set_update},
            return_document=ReturnDocument.AFTER,
            **kwargs,
        )
        if not doc:
            raise DocumentNotFoundException()
        doc.pop("_id")

        self.logger.debug(f"updated one ({query}): {doc}")
        return doc  # type: ignore[no-any-return]

    async def update_set_many(self, query: dict, set_update: dict) -> int:
        """Update all matching docs."""
        self.logger.debug(f"update many with query: {query}")

        web_jsonschema_validate(set_update, self._schema_partial)
        res = await self._collection.update_many(query, {"$set": set_update})
        if not res.matched_count:
            raise DocumentNotFoundException()

        self.logger.debug(f"updated many: {query}")
        return res.modified_count

    ####################################################################
    # READS
    ####################################################################

    async def find_one(self, query: dict, **kwargs: Any) -> dict:
        """Find one matching the query."""
        self.logger.debug(f"finding one with query: {query}")

        doc = await self._collection.find_one(query, **kwargs)
        if not doc:
            raise DocumentNotFoundException()
        # https://pymongo.readthedocs.io/en/stable/faq.html#writes-and-ids
        doc.pop("_id")

        self.logger.debug(f"found one: {doc}")
        return doc  # type: ignore[no-any-return]

    async def find_all(self, query: dict, projection: list) -> AsyncIterator[dict]:
        """Find all matching the query."""
        self.logger.debug(f"finding with query: {query}")

        doc = {}
        async for doc in self._collection.find(query, projection):
            # https://pymongo.readthedocs.io/en/stable/faq.html#writes-and-ids
            doc.pop("_id")
            self.logger.debug(f"found {doc}")
            yield doc

        if not doc:
            self.logger.debug(f"found nothing matching query: {query}")
