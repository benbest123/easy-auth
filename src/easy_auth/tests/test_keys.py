from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)

from easy_auth.core.config import get_settings
from easy_auth.core.keys import compute_kid, get_key_by_kid, load_private_key


def test_compute_kid_deterministic() -> None:

    key = Ed25519PrivateKey.generate()

    assert compute_kid(key.public_key()) == compute_kid(key.public_key())


def test_diff_keys_diff_kids() -> None:

    key1 = Ed25519PrivateKey.generate()
    key2 = Ed25519PrivateKey.generate()

    assert compute_kid(key1.public_key()) != compute_kid(key2.public_key())


def test_missing_key_raises(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PRIVATE_KEY_PATH", str(tmp_path / "missing_key.pem"))
    get_settings.cache_clear()
    load_private_key.cache_clear()

    with pytest.raises(
        RuntimeError,
        match=f"No key at {tmp_path}/missing_key.pem — run 'uv run gen-keys'",
    ):
        load_private_key()


def test_get_key_by_kid_if_wrong() -> None:
    assert get_key_by_kid("wrong-kid") is None
