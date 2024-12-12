from logging import config as logging_config
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING


logging_config.dictConfig(LOGGING)

BASE_DIRECTORY = Path()


class Configs(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    project_name: str = Field(alias="PROJECT_NAME")

    pg_name: str = Field(alias="POSTGRES_DB", serialization_alias="DB_NAME")
    pg_user: str = Field(alias="POSTGRES_USER", serialization_alias="DB_USER")
    pg_password: str = Field(alias="POSTGRES_PASSWORD", serialization_alias="DB_PASSWORD")
    pg_host: str = Field(alias="POSTGRES_HOST", serialization_alias="DB_HOST")
    pg_port: int = Field(alias="POSTGRES_PORT", serialization_alias="DB_PORT")

    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: int = Field(alias="REDIS_PORT")

    mongo_host: str = Field(alias="MONGO_HOST_UGC", serialization_alias="DB_HOST")
    mongo_port: int = Field(alias="MONGO_PORT_UGC", serialization_alias="DB_PORT")
    mongo_name: str = Field(alias="MONGO_NAME_UGC", serialization_alias="DB_NAME")

    iters_password: int = Field(alias="ITERS_PASSWORD")
    hash_name_password: str = Field(alias="HASH_NAME_PASSWORD")

    producer_host: str = Field(alias="PRODUCER_HOST")
    producer_port: int = Field(alias="PRODUCER_PORT")

    email_confirmation_url: str = Field(alias="EMAIL_CONFIRMATION_URL")
    email_confirmation_lifetime_min: int = Field(alias="EMAIL_CONFIRMATION_LIFETIME_MIN")
    email_confirmation_redirect: str = Field(alias="EMAIL_CONFIRMATION_REDIRECT")

    ugc_host: str = Field(alias="UGC_HOST")
    ugc_port: str = Field(alias="UGC_PORT")

    auth_host: str = Field(alias="AUTH_HOST")
    auth_port: str = Field(alias="AUTH_PORT")

    jaeger_on: bool = Field(alias="JAEGER_ON")
    jaeger_host: str = Field(alias="JAEGER_HOST")
    jaeger_port: int = Field(alias="JAEGER_PORT")

    sentry_on: bool = Field(alias="SENTRY_ON")
    sentry_dsn: str = Field(alias="SENTRY_DSN")

    @property
    def postgres_dsn(self) -> str:
        return f"postgresql+psycopg://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_name}"

    @property
    def producer_dsn(self) -> str:
        return f"http://{self.producer_host}:{self.producer_port}/"

    @property
    def ugc_dsn(self) -> str:
        return f"http://{self.ugc_host}:{self.ugc_port}/"

    @property
    def auth_dsn(self) -> str:
        return f"http://{self.auth_host}:{self.auth_port}/"


class JWTConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    authjwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    authjwt_token_location: set[str] = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


class MiddlewareConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    update_time: int = Field(alias="UPDATE_TIME")
    update_val: int = Field(alias="UPDATE_VAL")
    capacity: int = Field(alias="CAPACITY")


configs = Configs()  # pyright: ignore[reportCallIssue]
jwt_config = JWTConfig()  # pyright: ignore[reportCallIssue]
middleware_config = MiddlewareConfig()  # pyright: ignore[reportCallIssue]
