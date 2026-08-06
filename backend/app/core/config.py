from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int = 8000

    mongodb_url: str
    mongodb_database: str

    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000"]
    )

    jwt_secret_key: SecretStr
    jwt_refresh_key: SecretStr
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 4
    registration_enabled: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    # Values required by Settings are supplied dynamically by the environment.
    return Settings()  # type: ignore[call-arg]
