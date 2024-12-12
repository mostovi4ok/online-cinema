from dataclasses import dataclass


type GangTopics = tuple[str, ...]


@dataclass(frozen=True)
class Analytics:
    api_kafka_change_qual: GangTopics = ("clickhouse",)
    api_kafka_click: GangTopics = ("clickhouse",)
    api_kafka_favourites: GangTopics = ("clickhouse", "postgres")
    api_kafka_filter: GangTopics = ("clickhouse",)
    api_kafka_moviestop: GangTopics = ("clickhouse",)
    api_kafka_rate: GangTopics = ("clickhouse", "postgres")
    api_kafka_review: GangTopics = ("clickhouse", "postgres")
    api_kafka_urltime: GangTopics = ("clickhouse",)


@dataclass(frozen=True)
class DataEmails:
    api_kafka_email_confirmation: GangTopics = ("instant_notification",)
    api_kafka_email_confirmation_dlq: GangTopics = ("instant_notification_dlq",)

    api_kafka_notification_new_films: GangTopics = ("leisurely_notification",)
    api_kafka_notification_new_films_dlq: GangTopics = ("leisurely_notification_dlq",)
    api_kafka_notification_new_series: GangTopics = ("instant_notification",)
    api_kafka_notification_new_series_dlq: GangTopics = ("instant_notification_dlq",)


@dataclass(frozen=True)
class Emails:
    api_kafka_email: GangTopics = ("instant_send",)
    api_kafka_email_dlq: GangTopics = ("instant_send_dlq",)


@dataclass(frozen=True)
class ProfileBell:
    api_kafka_notification_in_profile: GangTopics = ("leisurely_notification",)
    api_kafka_notification_in_profile_dlq: GangTopics = ("leisurely_notification_dlq",)


@dataclass(frozen=True)
class Topics(Analytics, DataEmails, Emails, ProfileBell): ...
