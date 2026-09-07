from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from easy_auth.core.config import get_settings
from easy_auth.core.keys import generate_key, load_private_key
from easy_auth.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def temp_key_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:

    key_path = tmp_path / "private.pem"
    generate_key(key_path)

    monkeypatch.setenv("PRIVATE_KEY_PATH", str(key_path))
    get_settings.cache_clear()
    load_private_key.cache_clear()
    yield key_path
    get_settings.cache_clear()
    load_private_key.cache_clear()
