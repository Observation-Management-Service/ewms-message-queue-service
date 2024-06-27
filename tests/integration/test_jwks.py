"""Test the JWKS mechanisms."""

import json
import logging
import os
from urllib.parse import urljoin

import cryptography
import jwt
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from rest_tools.client import RestClient
from rest_tools.utils.auth import _AuthValidate

LOGGER = logging.getLogger(__name__)


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


def test_jwks(rc: RestClient):
    """Test a normal interaction."""

    # write public and private files
    key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    with open(os.environ["BROKER_QUEUE_AUTH_PUBLIC_KEY_FILE"], "wb") as f:
        f.write(public_key)
    private_key = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(os.environ["BROKER_QUEUE_AUTH_PRIVATE_KEY_FILE"], "wb") as f:
        f.write(private_key)

    # get jwks
    auth = OpenIDAuthWithProviderInfo(
        rc.address,
        {
            "jwks_uri": urljoin(rc.address, "mqbroker-issuer/.well-known/jwks.json"),
        },
    )
    assert [
        obj.public_bytes(
            cryptography.hazmat.primitives.serialization.Encoding.PEM,
            cryptography.hazmat.primitives.serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        for obj in auth.public_keys.values()
    ] == [public_key]

    # get jwt & validate
    # token: dict = {}
    # auth.validate(token)

    # TODO - repeat with changed keys
