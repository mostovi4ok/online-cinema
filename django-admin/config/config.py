import logging
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIRECTORY = Path()


class Configs(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    secret_key: str = Field(alias="SECRET_KEY")

    debug: bool = Field(alias="DEBUG")

    movies_db_name: str = Field(alias="MOVIES_DB_NAME")
    movies_db_user: str = Field(alias="MOVIES_DB_USER")
    movies_db_password: str = Field(alias="MOVIES_DB_PASSWORD")
    movies_db_host: str = Field(alias="MOVIES_DB_HOST")
    movies_db_port: int = Field(alias="MOVIES_DB_PORT")

    auth_db_name: str = Field(alias="AUTH_DB_NAME")
    auth_db_user: str = Field(alias="AUTH_DB_USER")
    auth_db_password: str = Field(alias="AUTH_DB_PASSWORD")
    auth_db_host: str = Field(alias="AUTH_DB_HOST")
    auth_db_port: int = Field(alias="AUTH_DB_PORT")

    profile_db_name: str = Field(alias="PROFILE_DB_NAME")
    profile_db_user: str = Field(alias="PROFILE_DB_USER")
    profile_db_password: str = Field(alias="PROFILE_DB_PASSWORD")
    profile_db_host: str = Field(alias="PROFILE_DB_HOST")
    profile_db_port: int = Field(alias="PROFILE_DB_PORT")

    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: int = Field(alias="REDIS_PORT")

    django_superuser_username: str = Field(alias="DJANGO_SUPERUSER_USERNAME")
    django_superuser_email: str = Field(alias="DJANGO_SUPERUSER_EMAIL")
    django_superuser_password: str = Field(alias="DJANGO_SUPERUSER_PASSWORD")

    auth_api_login_url: str = Field(alias="AUTH_API_LOGIN_URL")
    admin_right_name: str = Field(alias="ADMIN_RIGHT_NAME")
    moderator_right_name: str = Field(alias="MODERATOR_RIGHT_NAME")

    sentry_on: bool = Field(alias="SENTRY_ON")
    sentry_dsn: str = Field(alias="SENTRY_DSN")

    producer_host: str = Field(alias="PRODUCER_HOST")
    producer_port: int = Field(alias="PRODUCER_PORT")

    @property
    def producer_dsn(self) -> str:
        return f"http://{self.producer_host}:{self.producer_port}/"


configs = Configs()  # pyright: ignore[reportCallIssue]


def init_logger() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="{process} - {asctime} - {levelname} - {filename} - [{name}:{funcName}] on line {lineno}\n[{message}]",
        datefmt="%d/%m/%Y %H:%M:%S",
        style="{",
    )
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


logger = init_logger()
