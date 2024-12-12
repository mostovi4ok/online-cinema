from http import HTTPStatus
from typing import Literal
from uuid import UUID

import requests
from flask import Blueprint, jsonify, request
from flask.wrappers import Response
from flask_jwt_extended import jwt_required, verify_jwt_in_request

from core.config import configs
from services.redis_service import get_redis_service


analytics_bp = Blueprint("auth", __name__)
redis_service = get_redis_service()


@analytics_bp.route("/analytics", methods=["POST"])
@jwt_required()
def analytics() -> (
    tuple[Response, Literal[HTTPStatus.UNAUTHORIZED]]
    | tuple[Response, int]
    | tuple[Response, Literal[HTTPStatus.IM_A_TEAPOT]]
    | Response
):
    # Проверка токена
    _, jwt_data = verify_jwt_in_request() or (None, None)
    if jwt_data is None or redis_service.check_banned_access(
        UUID(jwt_data["sub"]), request.cookies["access_token_cookie"]
    ):
        return jsonify({"error": "Unauthorized"}), HTTPStatus.UNAUTHORIZED

    try:
        response = requests.post(
            f"{configs.producer_dsn}api/v1/producer",
            params=dict(request.args),
            json=request.get_json(),
            timeout=(3, 10),
        )
    except OSError:
        return jsonify({"error": "Producer did not respond"}), HTTPStatus.SERVICE_UNAVAILABLE

    return jsonify(response.json()), response.status_code


@analytics_bp.route("/")
def hello_world() -> Literal["<p>Hello, World!</p>"]:
    _ = 1 / 0  # raises an error for Sentry test
    return "<p>Hello, World!</p>"
