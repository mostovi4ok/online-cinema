from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any

import sentry_sdk
from async_fastapi_jwt_auth.auth_jwt import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from elasticsearch import AsyncElasticsearch
from fastapi import Depends, FastAPI, Request, Response, status
from fastapi.logger import logger
from fastapi.responses import JSONResponse, ORJSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.trace import get_tracer
from opentelemetry.trace.propagation import get_current_span
from redis.asyncio import Redis
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from api.v1 import films, genres, persons
from core.config import JWTConfig, configs, jwt_config
from core.jaeger_configure import configure_tracer
from db import elastic, redis
from jwt_auth_helpers import get_jwt_user_global
from services.errors import ContentError


@AuthJWT.load_config
def get_config() -> JWTConfig:
    return jwt_config


tags_metadata = [
    films.films_tags_metadata,
    genres.genres_tags_metadata,
    persons.persons_tags_metadata,
]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    redis.redis = Redis(host=configs.redis_host, port=configs.redis_port)
    elastic.es = AsyncElasticsearch(hosts=[configs.elastic_dsn])
    yield
    await redis.redis.close()
    await elastic.es.close()


if configs.sentry_on:
    sentry_sdk.init(
        dsn=configs.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        integrations=[
            StarletteIntegration(
                transaction_style="endpoint",
                failed_request_status_codes={403, *range(500, 599)},
                http_methods_to_capture=("GET",),
            ),
            FastApiIntegration(
                transaction_style="endpoint",
                failed_request_status_codes={403, *range(500, 599)},
                http_methods_to_capture=("GET",),
            ),
        ],
    )


app = FastAPI(
    title=configs.project_name,
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    openapi_tags=tags_metadata,
    redoc_url="/api/redoc",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@app.get("/sentry-debug")
async def trigger_error() -> None:
    _ = 1 / 0


if configs.jaeger_on:
    FastAPIInstrumentor.instrument_app(app)

    configure_tracer()

    tracer = get_tracer(app.title)

    @app.middleware("http")
    @tracer.start_as_current_span(app.title)
    async def before_request(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request_id = request.headers.get("X-Request-Id")
        if request_id is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "X-Request-Id is required"})

        response = await call_next(request)
        get_current_span().set_attribute("http.request_id", request_id)
        logger.info(f"{request_id}: {request.method} {request.url} {response.status_code}")
        return response


@app.exception_handler(ContentError)
async def edo_fatal_error_handler(request: Request, exc: ContentError) -> JSONResponse:  # noqa: RUF029
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": exc.message})


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(films.router, prefix="/api/v1/films", dependencies=[Depends(get_jwt_user_global)])
app.include_router(genres.router, prefix="/api/v1/genres", dependencies=[Depends(get_jwt_user_global)])
app.include_router(persons.router, prefix="/api/v1/persons", dependencies=[Depends(get_jwt_user_global)])
