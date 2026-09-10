from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from easy_auth.core.exceptions import (
    ClientNotFoundError,
)
from easy_auth.models.client import Client
from easy_auth.models.membership import Membership
from easy_auth.models.user import User


async def get_active_client(session: AsyncSession, client_id: str) -> Client:
    client_lookup = select(Client).where(Client.client_id == client_id)
    client_lookup_result = await session.execute(client_lookup)
    client = client_lookup_result.scalar_one_or_none()
    if not client:
        raise ClientNotFoundError(f"client {client_id} not found")

    if not client.is_active:
        raise ClientNotFoundError(f"client {client_id} is not active")

    return client


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    user_lookup = select(User).where(User.email == email)
    user_lookup_result = await session.execute(user_lookup)
    return user_lookup_result.scalar_one_or_none()


async def get_membership_by_client_user(
    session: AsyncSession, client_id: str, user_id: UUID
) -> Membership | None:
    membership_lookup = select(Membership).where(
        Membership.client_id == client_id, Membership.user_id == user_id
    )
    membership_lookup_result = await session.execute(membership_lookup)
    return membership_lookup_result.scalar_one_or_none()
