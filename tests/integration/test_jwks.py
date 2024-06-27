"""Test the JWKS mechanisms."""

import json
import logging
import os
from urllib.parse import urljoin

import cryptography
import jwt
import requests
from rest_tools.client import RestClient
from rest_tools.utils.auth import _AuthValidate

from .utils import refresh_mqbroker_key_files

LOGGER = logging.getLogger(__name__)

ROUTE_VERSION_PREFIX = "v0"


class OpenIDAuthWithProviderInfo(_AuthValidate):
    """Handle validation of JWT tokens using OpenID .well-known auto-discovery."""

    def __init__(
        self,
        url: str,
        provider_info: dict[str, str | list[str]] | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.url = url if url.endswith("/") else url + "/"
        self.public_keys: dict[
            str, cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey
        ] = {}
        self.provider_info = provider_info if provider_info else {}
        self.token_url: str | None = None

        self._refresh_keys()

    def _refresh_keys(self):
        try:
            if not self.provider_info:
                # discovery
                r = requests.get(self.url + ".well-known/openid-configuration")
                r.raise_for_status()
                self.provider_info = r.json()

                # get token url
                self.token_url = self.provider_info["token_endpoint"]

            # get keys
            r = requests.get(self.provider_info["jwks_uri"])
            r.raise_for_status()
            for jwk in r.json()["keys"]:
                LOGGER.debug(f"jwk: {jwk}")
                kid = jwk["kid"]
                LOGGER.debug(f"loaded JWT key {kid}")
                self.public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(
                    json.dumps(jwk)
                )
        except Exception:
            LOGGER.warning("failed to refresh OpenID keys", exc_info=True)

    def validate(self, token, **kwargs):
        """
        Validate a token.

        Args:
            token (str): a JWT token
            audience (str): audience, or None to disable audience verification

        Returns:
            dict: data inside token

        Raises:
            Exception on failure to validate.
        """
        header = jwt.get_unverified_header(token)
        if header["kid"] not in self.public_keys:
            self._refresh_keys()
        if header["kid"] in self.public_keys:
            key = self.public_keys[header["kid"]]
            return self._validate(token, key, **kwargs)
        else:
            raise Exception(f'JWT key {header["kid"]} not found')


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
        auth = OpenIDAuthWithProviderInfo(
            rc.address,
            {
                "jwks_uri": urljoin(
                    rc.address, "mqbroker-issuer/.well-known/jwks.json"
                ),
            },
        )
        assert sorted(
            obj.public_bytes(
                cryptography.hazmat.primitives.serialization.Encoding.PEM,
                cryptography.hazmat.primitives.serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            for obj in auth.public_keys.values()
        ) == sorted(all_public_keys)

        # get jwt(s) & validate
        workflow_id = "abc123"
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
