from logging import config as logging_config
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING


# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


BASE_DIRECTORY = Path()


class Configs(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    project_name: str = Field(alias="PROJECT_NAME")

    es_host: str = Field(alias="ELASTIC_HOST")
    es_port: int = Field(alias="ELASTIC_PORT")

    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: int = Field(alias="REDIS_PORT")
    redis_cache_expire_in_seconds: int = Field(alias="REDIS_CACHE_EXPIRE_IN_SECONDS")

    subscriber_right_name: str = Field(alias="SUBSCRIBER_RIGHT_NAME")

    jaeger_on: bool = Field(alias="JAEGER_ON")
    jaeger_host: str = Field(alias="JAEGER_HOST")
    jaeger_port: int = Field(alias="JAEGER_PORT")

    sentry_on: bool = Field(alias="SENTRY_ON")
    sentry_dsn: str = Field(alias="SENTRY_DSN")

    @property
    def elastic_dsn(self) -> str:
        return f"http://{self.es_host}:{self.es_port}/"


class JWTConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    authjwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    authjwt_token_location: set[str] = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


configs = Configs()  # pyright: ignore[reportCallIssue]
jwt_config = JWTConfig()  # pyright: ignore[reportCallIssue]
