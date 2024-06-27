"""Utilities for integration tests."""

import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def refresh_mqbroker_key_files() -> tuple[bytes, bytes]:
    """Write public and private files."""
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

    return public_key, private_key
