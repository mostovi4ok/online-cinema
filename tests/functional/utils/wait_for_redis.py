import backoff
from redis import ConnectionError as RedisConnectionError
from redis import Redis

from core.settings import test_settings


@backoff.on_exception(backoff.expo, RedisConnectionError, max_tries=10)
def wait_for_redis() -> None:
    if not Redis(host=test_settings.redis_host, port=test_settings.redis_port).ping():
        raise RedisConnectionError("Elasticsearch is not running.")


if __name__ == "__main__":
    wait_for_redis()
