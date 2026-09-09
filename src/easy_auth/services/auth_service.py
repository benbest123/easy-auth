from sqlalchemy.ext.asyncio import AsyncSession

from easy_auth.core.security import hash_password
from easy_auth.models.membership import Membership
from easy_auth.models.user import User
from easy_auth.services.queries import (
    get_active_client,
    get_membership_by_client_user,
    get_user_by_email,
)


# register service, returns bool denoting pending_approval (aka auto_provision on/off)
async def register(
    session: AsyncSession, email: str, password: str, client_id: str
) -> bool:

    client = await get_active_client(session, client_id)

    password_hash = hash_password(password)

    # lookup user by email
    user = await get_user_by_email(session, email)

    membership = None  # assign here so membership is not unbounded for new users

    # new user -> register user
    if not user:
        user = User(email=email, password_hash=password_hash)
        session.add(user)
        await session.flush()  # inserts without committing so we can use user_id

    # lookup membership for user/client if not new user
    else:
        membership = await get_membership_by_client_user(
            session, client.client_id, user.user_id
        )

    if not membership and client.auto_provision:
        membership = Membership(user_id=user.user_id, client_id=client.client_id)
        session.add(membership)

    # existing user, existing membership -> do nothing

    await session.commit()

    pending_approval = not client.auto_provision

    return pending_approval
