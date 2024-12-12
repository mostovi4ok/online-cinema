from typing import TYPE_CHECKING

from sqlalchemy import select

from db.models_sql import Right, Template, User
from db.postgres_db import get_admin_session, get_auth_session
from models.send_models import SendEmail


if TYPE_CHECKING:
    from models.task_models import (
        ApiKafkaEmailConfirmation,
        ApiKafkaNotificationNewFilms,
        ApiKafkaNotificationNewSeries,
    )


async def get_template(contract_name: str) -> Template:
    stmt = select(Template).where(Template.contract_name == contract_name)
    return (await get_admin_session().scalars(stmt)).one()


async def email_confirmation(task: "ApiKafkaEmailConfirmation") -> SendEmail:
    assert task.key is not None
    key = task.key
    template = await get_template(key)

    return SendEmail(
        notification_id=task.notification_id,
        subject=template.subject,
        content=template.content,
        recipient_variables={task.user_email: {"id": 1, "user_email": task.user_email, "link": task.link}},
    )


async def email_new_films(task: "ApiKafkaNotificationNewFilms") -> SendEmail:
    assert task.key is not None
    key = task.key
    template = await get_template(key)

    stmt = select(User.email).join_from(User, Right).where(Right.name == task.user_group)
    emails = (await get_auth_session().scalars(stmt)).all()
    recipient_variables = {email: {"id": i, "link": task.link} for i, email in enumerate(emails, 1)}
    return SendEmail(subject=template.subject, content=template.content, recipient_variables=recipient_variables)


async def email_new_series(task: "ApiKafkaNotificationNewSeries") -> SendEmail:
    assert task.key is not None
    key = task.key
    template = await get_template(key)

    emails = (await get_auth_session().scalars(select(User.email))).all()
    recipient_variables = {email: {"id": i, "link": task.link} for i, email in enumerate(emails, 1)}
    return SendEmail(subject=template.subject, content=template.content, recipient_variables=recipient_variables)
