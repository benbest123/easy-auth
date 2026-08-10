import argparse
import sys

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from easy_auth.core.config import get_settings
from easy_auth.core.keys import compute_kid


def main() -> None:

    parser = argparse.ArgumentParser(description="Generate an Ed25519 signing keypair")
    parser.add_argument(
        "--force", action="store_true", help="Overwrite an existing key"
    )
    args = parser.parse_args()

    key_path = get_settings().private_key_path

    if key_path.exists() and not args.force:
        print(
            f"Key already exists at {key_path} — refusing to overwrite. Pass --force to regenerate.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    key_path.parent.mkdir(parents=True, exist_ok=True)

    # generate private key and write to disk
    private_key = ed25519.Ed25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    key_path.write_bytes(private_bytes)
    key_path.chmod(0o600)  # owner read/write only

    public_key = private_key.public_key()
    kid = compute_kid(public_key)

    print(kid)
