from uuid import UUID, uuid4

from sqlalchemy import Index, text
from sqlalchemy.orm import Mapped, mapped_column

from easy_auth.core.db import Base
from easy_auth.models.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = (Index("ix_users_email_lower", text("lower(email)"), unique=True),)

    user_id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    email: Mapped[str]
    password_hash: Mapped[str]
    email_verified: Mapped[bool] = mapped_column(default=False)
