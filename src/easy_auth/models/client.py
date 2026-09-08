from sqlalchemy import String, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from easy_auth.models.mixins import Base, TimestampMixin


class Client(Base, TimestampMixin):
    __tablename__ = "clients"

    client_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    allowed_redirect_origins: Mapped[list[str]] = mapped_column(
        ARRAY(String), default=list
    )
    auto_provision: Mapped[bool] = mapped_column(
        default=True, server_default=text("true")
    )
    cors_origins: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    secret_hash: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))
