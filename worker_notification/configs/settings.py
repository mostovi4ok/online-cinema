from logging import Logger, getLogger
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIRECTORY = Path()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    producer_host: str = Field(alias="PRODUCER_HOST")
    producer_port: int = Field(alias="PRODUCER_PORT")

    kafka_servers: list[str] | str = Field(alias="KAFKA_SERVERS")
    kafka_topics: list[str] = Field(alias="KAFKA_TOPICS")
    kafka_group_id: str = Field(alias="KAFKA_GROUP_ID")
    kafka_max_records: int = Field(alias="KAFKA_MAX_RECORDS")

    run_interval_seconds: int = Field(alias="RUN_INTERVAL_SECONDS")
    scheduler_max_instances: int = Field(alias="SCHEDULER_MAX_INSTANCES")
    log_level: str = Field(alias="LOG_LEVEL")

    logger: Logger = getLogger("etl")

    sentry_on: bool = Field(alias="SENTRY_ON")
    sentry_dsn: str = Field(alias="SENTRY_DSN")

    postgres_db_name_admin: str = Field(alias="POSTGRES_DB_NAME_ADMIN")
    postgres_db_user_admin: str = Field(alias="POSTGRES_DB_USER_ADMIN")
    postgres_db_password_admin: str = Field(alias="POSTGRES_DB_PASSWORD_ADMIN")
    postgres_db_host_admin: str = Field(alias="POSTGRES_DB_HOST_ADMIN")
    postgres_db_port_admin: int = Field(alias="POSTGRES_DB_PORT_ADMIN")

    postgres_db_name_auth: str = Field(alias="POSTGRES_DB_NAME_AUTH")
    postgres_db_user_auth: str = Field(alias="POSTGRES_DB_USER_AUTH")
    postgres_db_password_auth: str = Field(alias="POSTGRES_DB_PASSWORD_AUTH")
    postgres_db_host_auth: str = Field(alias="POSTGRES_DB_HOST_AUTH")
    postgres_db_port_auth: int = Field(alias="POSTGRES_DB_PORT_AUTH")

    mongo_host: str = Field(alias="MONGO_HOST_UGC", serialization_alias="DB_HOST")
    mongo_port: int = Field(alias="MONGO_PORT_UGC", serialization_alias="DB_PORT")
    mongo_name: str = Field(alias="MONGO_NAME_UGC", serialization_alias="DB_NAME")

    dlq_notification: str = "dlq_notification"

    @property
    def producer_dsn(self) -> str:
        return f"http://{self.producer_host}:{self.producer_port}/"

    @property
    def postgres_dsn_admin(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_db_user_admin}:{self.postgres_db_password_admin}@{self.postgres_db_host_admin}:"
            f"{self.postgres_db_port_admin}/{self.postgres_db_name_admin}"
        )

    @property
    def postgres_dsn_auth(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_db_user_auth}:{self.postgres_db_password_auth}@{self.postgres_db_host_auth}:"
            f"{self.postgres_db_port_auth}/{self.postgres_db_name_auth}"
        )


settings = Settings()  # pyright: ignore[reportCallIssue]
