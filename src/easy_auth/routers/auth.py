from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from easy_auth.core.db import get_db
from easy_auth.schemas.auth import RegisterRequest, RegisterResponse
from easy_auth.services.auth_service import register

router = APIRouter(prefix="/auth", tags=["auth"])

SessionDep = Annotated[AsyncSession, Depends(get_db)]


@router.post("/register", status_code=201, response_model=RegisterResponse)
async def register_user(body: RegisterRequest, session: SessionDep) -> RegisterResponse:

    pending_approval = await register(
        session, body.email, body.password, body.client_id
    )

    return RegisterResponse(email=body.email, pending_approval=pending_approval)
