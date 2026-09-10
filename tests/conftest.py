from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from easy_auth.core.config import get_settings
from easy_auth.core.db import get_db
from easy_auth.core.keys import generate_key, load_private_key
from easy_auth.main import app
from easy_auth.models.client import Client


@pytest.fixture
async def async_client(session: AsyncSession) -> AsyncIterator[AsyncClient]:
    app.dependency_overrides[get_db] = lambda: session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
async def session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(
        get_settings().database_url.get_secret_value(), poolclass=NullPool
    )
    async with engine.connect() as connection:
        transaction = await connection.begin()
        factory = async_sessionmaker(bind=connection, expire_on_commit=False)
        async with factory() as s:
            yield s

        await transaction.rollback()
    await engine.dispose()


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


@pytest.fixture
def make_client(session: AsyncSession) -> Callable[..., Awaitable[Client]]:
    async def _make(client_id: str = "test-client", **kwargs) -> Client:
        client = Client(client_id=client_id, name="Test Client", **kwargs)
        session.add(client)
        await session.flush()
        return client

    return _make
