import random
import uuid

from faker import Faker


fake = Faker("en_US")

ClickData = dict[str, str | int]
UrlTimeData = dict[str, str | int]
FilmTimeData = dict[str, str | int]
SearchData = dict[str, str | int | list[str]]
ChangeQualData = dict[str, str | int]
FeedbackData = dict[str, str | int]
FavouritesData = dict[str, str]

MESS_NUM = 2
CLICK_NUM = 1002


def generate_click_data(num_clicks: int) -> list[ClickData]:
    click_data: list[dict[str, str | int]] = [
        {
            "user_id": str(uuid.uuid4()),
            "element_id": str(uuid.uuid4()),
            "group_id": str(uuid.uuid4()),
            "time": str(fake.date_time()),
        }
        for _ in range(num_clicks)
    ]
    click_data.append({
        "user_id": 0,
        "element_id": 1,
        "group_id": 2,
        "time": 3,
    })
    return click_data


def generate_urltime_data(num_entries: int) -> list[UrlTimeData]:
    return [
        {
            "user_id": str(uuid.uuid4()),
            "url": str(fake.url()),
            "spent_time": random.randint(1, 50000),
        }
        for _ in range(num_entries)
    ]


def generate_change_qual(num_entries: int) -> list[ChangeQualData]:
    return [
        {
            "user_id": str(uuid.uuid4()),
            "film_id": str(uuid.uuid4()),
            "prev_qual": random.randint(144, 2160),
            "new_qual": random.randint(144, 2160),
        }
        for _ in range(num_entries)
    ]


def generate_filmtime_data() -> list[FilmTimeData]:
    return [
        {
            "user_id": str(uuid.uuid4()),
            "film_id": str(uuid.uuid4()),
            "action": "stop",
            "film_curr_time": random.randint(1, 20000),
            "film_abs_time": random.randint(1, 20000),
        },
        {
            "user_id": str(uuid.uuid4()),
            "film_id": str(uuid.uuid4()),
            "action": "pause",
            "film_curr_time": random.randint(1, 20000),
            "film_abs_time": random.randint(1, 20000),
        },
    ]


def generate_search_data(num_entries: int) -> list[SearchData]:
    return [
        {
            "user_id": str(uuid.uuid4()),
            "film_id": str(uuid.uuid4()),
            "filter_id_genre": [str(uuid.uuid4()), str(uuid.uuid4())],
            "filter_rating": 5,
            "filter_id_actor": [str(uuid.uuid4()), str(uuid.uuid4())],
        }
        for _ in range(num_entries)
    ]


CLICK_DATA = generate_click_data(CLICK_NUM)
URLTIME_DATA = generate_urltime_data(MESS_NUM)
CHANGE_QUAL_DATA = generate_change_qual(MESS_NUM)
FILMTIME_DATA = generate_filmtime_data()
SEARCH_DATA = generate_search_data(MESS_NUM)
