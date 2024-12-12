from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from collectors import collector_email, collector_profile
from handlers.handlers_email import (
    email_confirmation,
    email_new_films,
    email_new_series,
)


if TYPE_CHECKING:
    from models.send_models import SendEmail


type MethodSend = Literal["email", "profile", "push", "sms", "websocket", "social_network"]
type Task = (
    ApiKafkaEmailConfirmation
    | ApiKafkaNotificationNewFilms
    | ApiKafkaNotificationNewSeries
    | ApiKafkaNotificationInProfile
)
type Email = ApiKafkaEmailConfirmation | ApiKafkaNotificationNewFilms | ApiKafkaNotificationNewSeries
type Profile = ApiKafkaNotificationInProfile


@dataclass(frozen=True)
class FunctionsSend:
    email: tuple[Callable[[list[Email]], Coroutine[Any, Any, None]], str] = collector_email, "api_kafka_email"
    profile: tuple[Callable[[list[Profile]], Coroutine[Any, Any, None]], str] = collector_profile, ""
    push: tuple[Callable[[list[Task]], Coroutine[Any, Any, None]], str] | None = None
    sms: tuple[Callable[[list[Task]], Coroutine[Any, Any, None]], str] | None = None
    websocket: tuple[Callable[[list[Task]], Coroutine[Any, Any, None]], str] | None = None
    social_network: tuple[Callable[[list[Task]], Coroutine[Any, Any, None]], str] | None = None


@dataclass(frozen=True)
class Handlers:
    email: Callable[..., Coroutine[Any, Any, "SendEmail"]] | None = None
    profile: Callable[..., Coroutine[Any, Any, None]] | None = None
    push: Callable[..., Coroutine[Any, Any, Any]] | None = None
    sms: Callable[..., Coroutine[Any, Any, Any]] | None = None
    websocket: Callable[..., Coroutine[Any, Any, Any]] | None = None
    social_network: Callable[..., Coroutine[Any, Any, Any]] | None = None


class BaseTask(BaseModel):
    notification_id: UUID = Field(default_factory=uuid4)

    key: str | None = None
    key_send: str | None = None
    key_send_dlq: str | None = None
    value: Any | None = None

    method_send: MethodSend
    handlers: Handlers


class ApiKafkaEmailConfirmation(BaseTask):
    handlers: Handlers = Handlers(email=email_confirmation)
    method_send: MethodSend = "email"

    user_email: str
    link: str


class ApiKafkaNotificationNewFilms(BaseTask):
    handlers: Handlers = Handlers(email=email_new_films)

    user_group: str
    link: str


class ApiKafkaNotificationNewSeries(BaseTask):
    handlers: Handlers = Handlers(email=email_new_series)

    content_id: str
    series_number: str
    link: str


class ApiKafkaNotificationInProfile(BaseTask):
    handlers: Handlers = Handlers(profile=None)

    profile_id: UUID
    message: str
