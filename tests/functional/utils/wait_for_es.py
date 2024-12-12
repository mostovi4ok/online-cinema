import backoff
from elasticsearch import ConnectionError as ElasticConnectionError
from elasticsearch import Elasticsearch

from core.settings import test_settings


@backoff.on_exception(backoff.expo, ElasticConnectionError, max_tries=10)
def wait_for_es() -> None:
    if not Elasticsearch(hosts=test_settings.elastic_dsn).ping():
        raise ElasticConnectionError("Elasticsearch is not running.")


if __name__ == "__main__":
    wait_for_es()
