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

    access_token_min: int = Field(alias="ACCESS_TOKEN_MIN")
    refresh_token_min: int = Field(alias="REFRESH_TOKEN_MIN")

    iters_password: int = Field(alias="ITERS_PASSWORD")
    hash_name_password: str = Field(alias="HASH_NAME_PASSWORD")

    profile_api_host: str = Field(alias="PROFILE_API_HOST")
    profile_api_port: int = Field(alias="PROFILE_API_PORT")

    email_confirmation_url: str = Field(alias="EMAIL_CONFIRMATION_URL")
    email_confirmation_lifetime_min: int = Field(alias="EMAIL_CONFIRMATION_LIFETIME_MIN")
    email_confirmation_redirect: str = Field(alias="EMAIL_CONFIRMATION_REDIRECT")

    jaeger_on: bool = Field(alias="JAEGER_ON")
    jaeger_host: str = Field(alias="JAEGER_HOST")
    jaeger_port: int = Field(alias="JAEGER_PORT")

    sentry_on: bool = Field(alias="SENTRY_ON")
    sentry_dsn: str = Field(alias="SENTRY_DSN")

    @property
    def postgres_dsn(self) -> str:
        return f"postgresql+psycopg://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_name}"

    @property
    def profile_dsn(self) -> str:
        return f"http://{self.profile_api_host}:{self.profile_api_port}/"


class JWTConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    authjwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    authjwt_token_location: set[str] = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


class AdminConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    username: str = Field(alias="ADMIN_USERNAME")
    password: str = Field(alias="ADMIN_PASSWORD")
    right_name: str = Field(alias="ADMIN_RIGHT_NAME")
    email: str = Field(alias="ADMIN_EMAIL")


class OAuthConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    yandex_scope: str = Field(alias="YANDEX_SCOPE")
    yandex_state: str = Field(alias="YANDEX_STATE")
    yandex_client_id: str = Field(alias="YANDEX_CLIENT_ID")
    yandex_client_secret: str = Field(alias="YANDEX_CLIENT_SECRET")
    yandex_redirect_uri: str = Field(alias="YANDEX_REDIRECT_URI")

    google_scope: str = Field(alias="GOOGLE_SCOPE")
    google_state: str = Field(alias="GOOGLE_STATE")
    google_client_id: str = Field(alias="GOOGLE_CLIENT_ID")
    google_client_secret: str = Field(alias="GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str = Field(alias="GOOGLE_REDIRECT_URI")


class MiddlewareConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    update_time: int = Field(alias="UPDATE_TIME")
    update_val: int = Field(alias="UPDATE_VAL")
    capacity: int = Field(alias="CAPACITY")


configs = Configs()  # pyright: ignore[reportCallIssue]
jwt_config = JWTConfig()  # pyright: ignore[reportCallIssue]
admin_config = AdminConfig()  # pyright: ignore[reportCallIssue]
oauth_config = OAuthConfig()  # pyright: ignore[reportCallIssue]
middleware_config = MiddlewareConfig()  # pyright: ignore[reportCallIssue]
