from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from testdata.es_mapping import GENRE_SCHEMES_INDEX_ES, MOVIES_SCHEMES_INDEX_ES, PERSON_SCHEMES_INDEX_ES


BASE_DIRECTORY = Path()


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")

    es_host: str = Field(default="elasticsearch_db", alias="ELASTIC_HOST")
    es_port: int = Field(default=9200, alias="ELASTIC_PORT")
    es_id_field: str = Field(default="uuid", alias="ELASTIC_ID_FIELD")
    es_index_movies: str = Field(default="movies", alias="ELASTIC_INDEX_MOVIES")
    es_index_mapping_movies: dict[Any, Any] = Field(
        default=MOVIES_SCHEMES_INDEX_ES, alias="ELASTIC_INDEX_MAPPING_MOVIES"
    )
    es_index_genres: str = Field(default="genres", alias="ELASTIC_INDEX_GENRES")
    es_index_mapping_genres: dict[Any, Any] = Field(
        default=GENRE_SCHEMES_INDEX_ES, alias="ELASTIC_INDEX_MAPPING_GENRES"
    )
    es_index_persons: str = Field(default="persons", alias="ELASTIC_INDEX_PERSONS")
    es_index_mapping_persons: dict[Any, Any] = Field(
        default=PERSON_SCHEMES_INDEX_ES, alias="ELASTIC_INDEX_MAPPING_PERSONS"
    )

    redis_host: str = Field(default="redis_db", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")

    kafka_urls: list[str] | str = Field(default=["kafka-0:9092", "kafka-1:9092", "kafka-2:9092"], alias="KAFKA_URL")
    kafka_topics: list[str] = Field(default=["instant_notification"], alias="KAFKA_TOPICS")
    kafka_group_id: str = Field(default="tests", alias="KAFKA_GROUP_ID")
    kafka_max_records: int = Field(default=1000, alias="KAFKA_MAX_RECORDS")

    auth_pg_name: str = Field(default="auth_database", alias="AUTH_POSTGRES_DB", serialization_alias="DB_NAME")
    auth_pg_user: str = Field(default="postgres", alias="AUTH_POSTGRES_USER", serialization_alias="DB_USER")
    auth_pg_password: str = Field(default="123qwe", alias="AUTH_POSTGRES_PASSWORD", serialization_alias="DB_PASSWORD")
    auth_pg_host: str = Field(default="postgres_db_auth", alias="AUTH_POSTGRES_HOST", serialization_alias="DB_HOST")
    auth_pg_port: int = Field(default=5432, alias="AUTH_POSTGRES_PORT", serialization_alias="DB_PORT")

    profile_pg_name: str = Field(default="profile_database", alias="PROFILE_POSTGRES_DB", serialization_alias="DB_NAME")
    profile_pg_user: str = Field(default="postgres", alias="PROFILE_POSTGRES_USER", serialization_alias="DB_USER")
    profile_pg_password: str = Field(
        default="123qwe", alias="PROFILE_POSTGRES_PASSWORD", serialization_alias="DB_PASSWORD"
    )
    profile_pg_host: str = Field(
        default="postgres_db_profile", alias="PROFILE_POSTGRES_HOST", serialization_alias="DB_HOST"
    )
    profile_pg_port: int = Field(default=5432, alias="PROFILE_POSTGRES_PORT", serialization_alias="DB_PORT")

    mongo_host: str = Field(default="mongos1", alias="MONGO_HOST_UGC", serialization_alias="DB_HOST")
    mongo_port: int = Field(default=27017, alias="MONGO_PORT_UGC", serialization_alias="DB_PORT")
    mongo_name: str = Field(default="UGCDB", alias="MONGO_NAME_UGC", serialization_alias="DB_NAME")

    iters_password: int = Field(default=100_000, alias="ITERS_PASSWORD")
    hash_name_password: str = Field(default="sha256", alias="HASH_NAME_PASSWORD")

    service_api_host: str = Field(default="api", alias="SERVICE_API_HOST")
    service_api_port: int = Field(default=8000, alias="SERVICE_API_PORT")

    service_auth_host: str = Field(default="auth_service", alias="SERVICE_AUTH_HOST")
    service_auth_port: int = Field(default=8000, alias="SERVICE_AUTH_PORT")

    service_profile_host: str = Field(default="profile_service", alias="SERVICE_PROFILE_HOST")
    service_profile_port: int = Field(default=8000, alias="SERVICE_PROFILE_PORT")

    service_ugc_host: str = Field(default="ugc_service", alias="SERVICE_UGC_HOST")
    service_ugc_port: int = Field(default=8000, alias="SERVICE_UGC_PORT")

    service_analytics_collector_host: str = Field(
        default="analytics_collector", alias="SERVICE_ANALYTICS_COLLECTOR_HOST"
    )
    service_analytics_collector_port: int = Field(default=5000, alias="SERVICE_ANALYTICS_COLLECTOR_PORT")

    @property
    def elastic_dsn(self) -> str:
        return f"http://{self.es_host}:{self.es_port}/"

    @property
    def auth_postgres_dsn(self) -> dict[str, str | int]:
        return {
            "dbname": self.auth_pg_name,
            "user": self.auth_pg_user,
            "password": self.auth_pg_password,
            "host": self.auth_pg_host,
            "port": self.auth_pg_port,
        }

    @property
    def auth_postgres_url(self) -> str:
        return f"postgresql+psycopg://{self.auth_pg_user}:{self.auth_pg_password}@{self.auth_pg_host}:{self.auth_pg_port}/{self.auth_pg_name}"

    @property
    def profile_postgres_dsn(self) -> dict[str, str | int]:
        return {
            "dbname": self.profile_pg_name,
            "user": self.profile_pg_user,
            "password": self.profile_pg_password,
            "host": self.profile_pg_host,
            "port": self.profile_pg_port,
        }

    @property
    def profile_postgres_url(self) -> str:
        return f"postgresql+psycopg://{self.profile_pg_user}:{self.profile_pg_password}@{self.profile_pg_host}:{self.profile_pg_port}/{self.profile_pg_name}"

    @property
    def service_api_url(self) -> str:
        return f"http://{self.service_api_host}:{self.service_api_port}/"

    @property
    def service_auth_url(self) -> str:
        return f"http://{self.service_auth_host}:{self.service_auth_port}/"

    @property
    def service_profile_url(self) -> str:
        return f"http://{self.service_profile_host}:{self.service_profile_port}/"

    @property
    def service_ugc_url(self) -> str:
        return f"http://{self.service_ugc_host}:{self.service_ugc_port}/"

    @property
    def service_analytics_collector_url(self) -> str:
        return f"http://{self.service_analytics_collector_host}:{self.service_analytics_collector_port}/"


test_settings = TestSettings()
