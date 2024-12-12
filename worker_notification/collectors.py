from collections import defaultdict
from typing import TYPE_CHECKING, Any

from db.models_mongo import ProfileBell, State
from sender import pack_and_send


if TYPE_CHECKING:
    from models.task_models import Email, Profile


async def collector_email(tasks: "list[Email]") -> None:
    ready_messages: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    not_ready_messages: defaultdict[str, list[Email]] = defaultdict(list)
    for task in tasks:
        assert task.key_send is not None
        key = task.key_send
        if (email := task.handlers.email) is None:
            continue

        state = await State.insert_one(State(notification_id=task.notification_id))
        assert state is not None
        ready_messages[key].append((await email(task)).model_dump(mode="json"))
        not_ready_messages[key].append(task)

    for key, data in (await pack_and_send(ready_messages)).items():
        for answer, start, end in data:
            ready_bad_data: defaultdict[str, list[Any]] = defaultdict(list)
            if not answer and (not_ready_bad_data := not_ready_messages[key][start:end]):
                for bad_task in not_ready_bad_data:
                    assert bad_task.value is not None
                    assert bad_task.key_send_dlq is not None
                    ready_bad_data[bad_task.key_send_dlq].append(bad_task.value)

                await pack_and_send(ready_bad_data)


async def collector_profile(tasks: "list[Profile]") -> None:
    states: list[State] = []
    bells: list[ProfileBell] = []
    for task in tasks:
        states.append(State(notification_id=task.notification_id, send=True))
        bells.append(
            ProfileBell(notification_id=task.notification_id, profile_id=task.profile_id, message=task.message)
        )

    await ProfileBell.insert_many(bells)
    await State.insert_many(states)
