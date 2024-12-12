from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIRECTORY = Path()


class Configs(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: int = Field(alias="REDIS_PORT")

    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")

    producer_host: str = Field(alias="PRODUCER_HOST")
    producer_port: int = Field(alias="PRODUCER_PORT")

    sentry_on: bool = Field(alias="SENTRY_ON")
    sentry_dsn: str = Field(alias="SENTRY_DSN")

    @property
    def producer_dsn(self) -> str:
        return f"http://{self.producer_host}:{self.producer_port}/"


configs = Configs()  # pyright: ignore[reportCallIssue]
