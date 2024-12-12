import backoff
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from core.settings import test_settings


@backoff.on_exception(backoff.expo, NoBrokersAvailable, max_tries=10)
def connect_to_kafka() -> None:
    KafkaProducer(bootstrap_servers=test_settings.kafka_urls)


if __name__ == "__main__":
    connect_to_kafka()
