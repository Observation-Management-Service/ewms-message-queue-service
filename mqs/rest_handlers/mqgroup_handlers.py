"""REST handlers for actions on MQ groups."""

import logging
import time
import uuid

import mqclient
import tornado
from rest_tools.server import validate_request

from . import auth
from .base_handlers import BaseMQSHandler
from .. import config
from ..database.client import DocumentNotFoundException

LOGGER = logging.getLogger(__name__)


class MQGroupHandler(BaseMQSHandler):  # pylint: disable=W0223
    """The handler for creating MQ groups."""

    ROUTE = r"/mq-group$"

    @auth.service_account_auth(roles=[auth.AuthAccounts.WMS])  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def post(self) -> None:
        """Handle POST requests."""
        criteria: dict[str, int] = self.get_argument("criteria")

        mqgroup_id = uuid.uuid4().hex
        now = int(time.time())

        # insert mq group
        mqgroup = dict(
            mqgroup_id=mqgroup_id,
            timestamp=now,
            criteria=criteria,
        )
        await self.mqgroup_client.insert_one(mqgroup)

        # insert mq profiles
        mqprofiles = [
            dict(
                mqid=mqclient.Queue.make_name(),
                mqgroup_id=mqgroup_id,
                timestamp=now,
                nickname=f"mq-{mqgroup_id}-{i}",  # TODO: use user's values, like "input-queue"
            )
            for i in range(criteria["n_queues"])
        ]
        await self.mqprofile_client.insert_many(mqprofiles)

        self.write(
            dict(
                mqgroup=mqgroup,
                mqprofiles=mqprofiles,
            )
        )


class MQGroupIDHandler(BaseMQSHandler):  # pylint: disable=W0223
    """The handler for interacting with MQ groups."""

    ROUTE = r"/mq-group/(?P<mqgroup_id>\w+)$"

    @auth.service_account_auth(roles=[auth.AuthAccounts.WMS])  # type: ignore
    @validate_request(config.REST_OPENAPI_SPEC)  # type: ignore[misc]
    async def get(self, mqgroup_id: str) -> None:
        """Handle GET requests."""
        try:
            mqgroup = await self.mqgroup_client.find_one(dict(mqgroup_id=mqgroup_id))
        except DocumentNotFoundException:
            raise tornado.web.HTTPError(404, reason="MQGroup not found")

        self.write(mqgroup)
