from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    database_url: SecretStr

    private_key_path: Path

    issuer: str = "https://auth.benbest.uk"

    access_token_ttl_minutes: int = 15

    refresh_token_ttl_days: int = 7

    session_absolute_lifetime_days: int = 14

    environment: Literal["dev", "prod"] = "dev"

    require_verified_email: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
