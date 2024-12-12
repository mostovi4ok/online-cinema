from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIRECTORY = Path()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    pg_name: str = Field(alias="POSTGRES_DB", serialization_alias="DB_NAME")
    pg_user: str = Field(alias="POSTGRES_USER", serialization_alias="DB_USER")
    pg_password: str = Field(alias="POSTGRES_PASSWORD", serialization_alias="DB_PASSWORD")
    pg_host: str = Field(alias="POSTGRES_HOST", serialization_alias="DB_HOST")
    pg_port: int = Field(alias="POSTGRES_PORT", serialization_alias="DB_PORT")

    mongo_host: str = Field(alias="MONGO_HOST")
    mongo_port: int = Field(alias="MONGO_PORT")

    @property
    def postgres_dsn(self) -> dict[str, str | int]:
        return {
            "dbname": self.pg_name,
            "user": self.pg_user,
            "password": self.pg_password,
            "host": self.pg_host,
            "port": self.pg_port,
        }


settings = Settings()  # pyright: ignore[reportCallIssue]
