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

    sentry_on: bool = Field(alias="SENTRY_ON")
    sentry_dsn: str = Field(alias="SENTRY_DSN")

    from_email_address: str = Field(alias="FROM_EMAIL_ADDRESS")
    mailgun_api_url: str = Field(alias="MAILGUN_API_URL")
    mailgun_api_key: str = Field(alias="MAILGUN_API_KEY")

    mongo_host: str = Field(alias="MONGO_HOST_UGC", serialization_alias="DB_HOST")
    mongo_port: int = Field(alias="MONGO_PORT_UGC", serialization_alias="DB_PORT")
    mongo_name: str = Field(alias="MONGO_NAME_UGC", serialization_alias="DB_NAME")

    logger: Logger = getLogger("etl")

    @property
    def producer_dsn(self) -> str:
        return f"http://{self.producer_host}:{self.producer_port}/"


settings = Settings()  # pyright: ignore[reportCallIssue]
