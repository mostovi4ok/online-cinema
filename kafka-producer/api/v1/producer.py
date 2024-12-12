from http import HTTPStatus
from io import BytesIO
from os import listdir
from pathlib import Path
from typing import Literal

import backoff
from avro.datafile import DataFileWriter
from avro.io import DatumWriter
from avro.schema import Schema as AvroScheme
from avro.schema import parse as avro_parse
from flask import Blueprint, jsonify, request
from flask.wrappers import Response
from kafka import KafkaProducer
from kafka.errors import KafkaConnectionError, KafkaError

from api.v1.topics import GangTopics, Topics
from core.config import configs


analytics_bp = Blueprint("auth", __name__)
producer = KafkaProducer(bootstrap_servers=configs.kafka_urls, api_version=(1, 1, 1))


# Загрузка схем Avro
schemas: dict[str, AvroScheme] = {}
for filename in listdir("contracts"):
    if filename.endswith(".avsc"):
        m_type = filename[:-5]
        schemas[m_type] = avro_parse((Path("contracts") / filename).read_text())


@analytics_bp.route("/producer", methods=["POST"])
def analytics() -> (
    tuple[Response, Literal[HTTPStatus.BAD_REQUEST]]
    | tuple[Response, Literal[HTTPStatus.REQUEST_ENTITY_TOO_LARGE]]
    | tuple[Response, Literal[HTTPStatus.UNPROCESSABLE_ENTITY]]
    | tuple[Response, Literal[HTTPStatus.SERVICE_UNAVAILABLE]]
    | Response
):
    # Получение схемы Avro
    m_type = request.args.get("message_type")
    if m_type is None:
        return jsonify({"error": "Missing message_type parameter"}), HTTPStatus.BAD_REQUEST

    schema = schemas.get(m_type)
    if schema is None:
        return jsonify({"error": f"Schema for {m_type} not found"}), HTTPStatus.BAD_REQUEST

    data = request.get_json()
    if len(data) > 1000:
        return jsonify({"error": "Too many records in the request"}), HTTPStatus.REQUEST_ENTITY_TOO_LARGE

    # Сериализация данных в Avro
    try:
        with BytesIO() as bytes_writer:
            data_file_writer = DataFileWriter(bytes_writer, DatumWriter(), schema)
            for record in data:
                data_file_writer.append(record)

            data_file_writer.flush()
            bytes_data = bytes_writer.getvalue()
    except Exception as e:  # noqa: BLE001
        return jsonify({"error": f"Avro data serialization error: {e}"}), HTTPStatus.UNPROCESSABLE_ENTITY

    m_topics: GangTopics = getattr(Topics, m_type)
    # Отправка сообщения в Kafka
    try:
        send_kafka(m_topics, bytes_data, m_type)
    except KafkaError as e:
        return jsonify({"error": f"Error writing data to Kafka: {e}"}), HTTPStatus.SERVICE_UNAVAILABLE

    return jsonify({"status": "OK"})


@backoff.on_exception(backoff.expo, KafkaConnectionError, max_tries=10, max_time=10)
def send_kafka(m_topics: GangTopics, bytes_data: bytes, m_type: str) -> None:
    for m_topic in m_topics:
        producer.send(topic=m_topic, value=bytes_data, key=m_type.encode())
        producer.flush()


@analytics_bp.route("/")
def hello_world() -> Literal["<p>Hello, World!</p>"]:
    _ = 1 / 0  # raises an error for Sentry test
    return "<p>Hello, World!</p>"
