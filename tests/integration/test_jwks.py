"""Test the JWKS mechanisms."""

import logging
import os
from urllib.parse import urljoin

from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from rest_tools.client import RestClient
from rest_tools.utils import OpenIDAuth

from .utils import refresh_mqbroker_key_files

LOGGER = logging.getLogger(__name__)

ROUTE_VERSION_PREFIX = "v0"


async def test_jwks(rc: RestClient):
    """Test a normal interaction."""

    with open(os.environ["BROKER_QUEUE_AUTH_PUBLIC_KEY_FILE"], "rb") as f:
        public_key = f.read()
    all_public_keys = [public_key]

    for i in range(5):  # arbitrary no. of loops
        if i > 0:
            public_key, _ = refresh_mqbroker_key_files()  # change keys
            all_public_keys.append(public_key)

        # get jwks
        auth = OpenIDAuth(
            rc.address,
            provider_info={
                "jwks_uri": urljoin(
                    rc.address, "mqbroker-issuer/.well-known/jwks.json"
                ),
            },
        )
        assert sorted(
            obj.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
            for obj in auth.public_keys.values()
        ) == sorted(all_public_keys)

        # get jwt(s) & validate
        workflow_id = f"workflowforjwkstesting{i}"
        queue_aliases = ["queue1", "queue2", "queue3"]
        public = ["queue1", "queue3"]
        # -> reserve mq group
        await rc.request(
            "POST",
            f"/{ROUTE_VERSION_PREFIX}/mqs/workflows/{workflow_id}/mq-group/reservation",
            {"queue_aliases": queue_aliases, "public": public},
        )
        # -> activate mq group
        resp = await rc.request(
            "POST",
            f"/{ROUTE_VERSION_PREFIX}/mqs/workflows/{workflow_id}/mq-group/activation",
            {"criteria": {"priority": 99}},
        )
        # -> validate jwt(s)
        for mqprofile in resp["mqprofiles"]:
            print(mqprofile["auth_token"])
            assert auth.validate(mqprofile["auth_token"])
