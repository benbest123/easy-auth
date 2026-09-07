import hashlib
import json
from base64 import urlsafe_b64encode
from functools import lru_cache
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from easy_auth.core.config import get_settings

JWK = dict[str, str]
JWKS = dict[str, list[JWK]]


def b64url(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode()


def _public_key_b64(public_key: Ed25519PublicKey) -> str:
    public_key_raw = public_key.public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )

    # raw bytes are not valid json text!
    return b64url(public_key_raw)


def compute_kid(public_key: Ed25519PublicKey) -> str:

    public_key_b64 = _public_key_b64(public_key)

    # building jwk - specifying edwards-curve family, specifically ed25519
    jwk = {"crv": "Ed25519", "kty": "OKP", "x": public_key_b64}

    # turn dict into byte exact string, hash it, make it printable
    canonical = json.dumps(jwk, sort_keys=True, separators=(",", ":")).encode()
    return b64url(hashlib.sha256(canonical).digest())


@lru_cache
def load_private_key() -> Ed25519PrivateKey:

    private_key_path = get_settings().private_key_path

    try:
        private_key = serialization.load_pem_private_key(
            private_key_path.read_bytes(), password=None
        )
    except FileNotFoundError:
        raise RuntimeError(
            f"No key at {private_key_path} — run 'uv run gen-keys'"
        ) from None

    if not isinstance(private_key, Ed25519PrivateKey):
        raise TypeError("Private key must be Ed25519")

    return private_key


def public_jwk(public_key: Ed25519PublicKey) -> JWK:

    public_key_b64 = _public_key_b64(public_key)

    # building jwk - specifying edwards-curve family, specifically ed25519
    jwk = {
        "crv": "Ed25519",
        "kty": "OKP",
        "x": public_key_b64,
        "kid": compute_kid(public_key),
        "alg": "EdDSA",
        "use": "sig",
    }

    return jwk


def get_jwks() -> JWKS:

    public_key = load_private_key().public_key()

    return {"keys": [public_jwk(public_key)]}


def get_signing_key() -> Ed25519PrivateKey:
    # for now is redundant, but will be used in future once we have rotation
    return load_private_key()


def get_key_by_kid(kid: str) -> Ed25519PublicKey | None:

    public_key = load_private_key().public_key()

    return public_key if compute_kid(public_key) == kid else None


def generate_key(key_path: Path) -> Ed25519PrivateKey:

    key_path.parent.mkdir(parents=True, exist_ok=True)

    # generate private key and write to disk
    private_key = Ed25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    key_path.write_bytes(private_bytes)
    key_path.chmod(0o600)  # owner read/write only

    return private_key
