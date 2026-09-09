from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, BeforeValidator, EmailStr, Field


def lower_case_email(v: object) -> str:
    return str(v).strip().lower()


LowerEmailStr = Annotated[EmailStr, BeforeValidator(lower_case_email)]


class RegisterRequest(BaseModel):
    email: LowerEmailStr
    password: str = Field(min_length=8, max_length=128)
    client_id: str


class RegisterResponse(BaseModel):
    user_id: UUID
    email: EmailStr
