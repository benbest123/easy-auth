from collections.abc import Awaitable, Callable

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from easy_auth.models.client import Client
from easy_auth.models.membership import Membership
from easy_auth.models.user import User
from easy_auth.services.queries import get_membership_by_client_user, get_user_by_email


async def test_register_new_user(
    async_client: AsyncClient,
    session: AsyncSession,
    make_client: Callable[..., Awaitable[Client]],
) -> None:
    await make_client()
    res = await async_client.post(
        "/auth/register",
        json={
            "email": "test1@example.com",
            "password": "testpassword",
            "client_id": "test-client",
        },
    )

    assert res.status_code == 201

    assert not res.json()["pending_approval"]

    user = await get_user_by_email(session, "test1@example.com")

    assert user is not None
    assert user.email == "test1@example.com"
    assert user.email_verified is False

    membership = await get_membership_by_client_user(
        session, "test-client", user.user_id
    )

    assert membership is not None
    assert membership.role == "user"


async def test_register_new_user_unknown_client(
    async_client: AsyncClient,
) -> None:
    res = await async_client.post(
        "/auth/register",
        json={
            "email": "test1@example.com",
            "password": "testpassword",
            "client_id": "unknown-client",
        },
    )

    assert res.status_code == 404


async def test_register_new_user_no_provision(
    async_client: AsyncClient,
    session: AsyncSession,
    make_client: Callable[..., Awaitable[Client]],
) -> None:
    await make_client("test-no-provision", auto_provision=False)
    res = await async_client.post(
        "/auth/register",
        json={
            "email": "test1@example.com",
            "password": "testpassword",
            "client_id": "test-no-provision",
        },
    )

    assert res.status_code == 201

    assert res.json()["pending_approval"]

    user = await get_user_by_email(session, "test1@example.com")

    assert user is not None
    assert user.email == "test1@example.com"
    assert user.email_verified is False

    membership = await get_membership_by_client_user(
        session, "test-no-provision", user.user_id
    )

    assert membership is None


async def test_register_existing_user_same_client(
    async_client: AsyncClient,
    session: AsyncSession,
    make_client: Callable[..., Awaitable[Client]],
) -> None:

    await make_client()

    test_email = "testexisting@example.com"
    body = {
        "email": test_email,
        "password": "testpassword",
        "client_id": "test-client",
    }

    # test that we get the same response when trying to register an already-existing
    # user on the same client
    first = await async_client.post("/auth/register", json=body)
    second = await async_client.post("/auth/register", json=body)

    assert first.status_code == second.status_code
    assert first.json() == second.json()

    user = await get_user_by_email(session, test_email)

    assert user is not None

    user_count = await session.scalar(
        select(func.count()).select_from(User).where(User.email == test_email)
    )
    membership_count = await session.scalar(
        select(func.count())
        .select_from(Membership)
        .where(Membership.user_id == user.user_id)
    )

    assert user_count == 1
    assert membership_count == 1


async def test_register_existing_user_different_client(
    async_client: AsyncClient,
    session: AsyncSession,
    make_client: Callable[..., Awaitable[Client]],
) -> None:

    await make_client("client-a")
    await make_client("client-b")

    test_email = "testexisting@example.com"

    first = await async_client.post(
        "/auth/register",
        json={"email": test_email, "password": "testpassword", "client_id": "client-a"},
    )
    second = await async_client.post(
        "/auth/register",
        json={"email": test_email, "password": "testpassword", "client_id": "client-b"},
    )

    assert first.status_code == 201
    assert second.status_code == 201

    user = await get_user_by_email(session, test_email)

    assert user is not None

    user_count = await session.scalar(
        select(func.count()).select_from(User).where(User.email == test_email)
    )
    membership_count = await session.scalar(
        select(func.count())
        .select_from(Membership)
        .where(Membership.user_id == user.user_id)
    )

    assert user_count == 1
    assert membership_count == 2
