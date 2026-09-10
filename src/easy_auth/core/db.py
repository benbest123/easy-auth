from collections.abc import AsyncIterator
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from easy_auth.core.config import get_settings

# lru_cache so file isnt read until first use
# allows tests to override url etc


@lru_cache
def get_engine() -> AsyncEngine:

    database_url = get_settings().database_url.get_secret_value()
    is_dev_env = get_settings().environment == "dev"

    return create_async_engine(database_url, echo=is_dev_env)


@lru_cache
def get_session_factory() -> async_sessionmaker[AsyncSession]:

    return async_sessionmaker(get_engine(), expire_on_commit=False)


async def get_db() -> AsyncIterator[AsyncSession]:
    session_factory = get_session_factory()
    async with session_factory() as session:
        yield session
