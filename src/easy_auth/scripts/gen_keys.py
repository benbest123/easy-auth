import argparse
import sys

from easy_auth.core.config import get_settings
from easy_auth.core.keys import compute_kid, generate_key


def main() -> None:

    parser = argparse.ArgumentParser(description="Generate an Ed25519 signing keypair")
    parser.add_argument(
        "--force", action="store_true", help="Overwrite an existing key"
    )
    args = parser.parse_args()

    key_path = get_settings().private_key_path

    if key_path.exists() and not args.force:
        print(
            f"Key already exists at {key_path} — refusing to overwrite. "
            "Pass --force to regenerate.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    # generate private key and write to disk
    private_key = generate_key(key_path)

    public_key = private_key.public_key()
    kid = compute_kid(public_key)

    print(f"key written to {key_path}")
    print(f"kid: {kid}")
