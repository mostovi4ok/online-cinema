import requests
from django.utils import timezone
from requests.exceptions import RequestException

from config.celery import app
from config.config import configs
from notifications.models import Task


@app.task  # pyright: ignore[reportUnknownMemberType]
def notification_manager() -> None:
    tasks = Task.objects.filter(started=False, time_start__lt=timezone.now())

    for task in tasks:
        try:
            template = task.template

            if template.contract_name == "api_kafka_notification_new_films":
                data = {
                    "user_group": template.content,
                    "link": "template_link",
                    "method_send": "email",
                }
            elif template.contract_name == "api_kafka_notification_new_series":
                data = {
                    "content_id": template.subject,
                    "series_number": template.content,
                    "link": "template_link",
                    "method_send": "email",
                }
            else:
                _handle_schema_error(task, template.contract_name)
                return

            response = requests.post(
                f"{configs.producer_dsn}api/v1/producer",
                json=data,
                params={"message_type": template.contract_name},
                timeout=(3, 10),
            )

            if response.status_code == 200:
                task.started = True
                task.save()
            else:
                _handle_api_error(task, response)

        except RequestException as req_ex:
            _handle_request_error(task, req_ex)
        except Exception as e:  # noqa: BLE001
            _handle_general_error(task, e)


def _handle_schema_error(task: Task, contract_name: str) -> None:
    print(f"Ошибка несоответствия схемы данных для задачи {task.name}: {contract_name}")


def _handle_api_error(task: Task, response: requests.Response) -> None:
    print(f"Ошибка отправки запроса к API для задачи {task.name}: {response.status_code} - {response.text}")


def _handle_request_error(task: Task, req_ex: RequestException) -> None:
    print(f"Ошибка при запросе к API для задачи {task.name}: {req_ex}")


def _handle_general_error(task: Task, e: Exception) -> None:
    print(f"Ошибка обработки задачи {task.name}: {e}")
