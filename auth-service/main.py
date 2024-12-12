import asyncio
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any, NoReturn

import sentry_sdk
from async_fastapi_jwt_auth.auth_jwt import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import Depends, FastAPI, Request, Response, status
from fastapi.logger import logger
from fastapi.responses import JSONResponse, ORJSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.trace import get_tracer
from opentelemetry.trace.propagation import get_current_span
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from api.v1 import access_control, auth, oauth
from core.config import JWTConfig, configs, jwt_config
from core.jaeger_configure import configure_tracer
from db.redis_db import get_redis
from jwt_auth_helpers import get_jwt_user_global
from middleware.token_bucket_middleware import TokenBucketMiddleware
from models.errors import ErrorBody
from services import redis_service
from services.custom_error import ResponseError
from services.token_bucket_service import get_token_bucket


@AuthJWT.load_config
def get_config() -> JWTConfig:
    return jwt_config


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    redis_service.redis = get_redis()

    background_tasks: set[asyncio.Task[NoReturn]] = set()
    token_bucket = get_token_bucket()
    task = asyncio.create_task(token_bucket.start_fill_bucket_process())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)

    yield

    task.cancel()
    await redis_service.redis.close()


tags_metadata = [
    auth.auth_tags_metadata,
    access_control.rights_tags_metadata,
]

responses: dict[str | int, Any] = {
    status.HTTP_421_MISDIRECTED_REQUEST: {"model": ErrorBody},
}


if configs.sentry_on:
    sentry_sdk.init(
        dsn=configs.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        integrations=[
            StarletteIntegration(
                transaction_style="endpoint",
                failed_request_status_codes={403, *range(500, 599)},
                http_methods_to_capture=("DELETE", "GET", "PATCH", "POST", "PUT"),
            ),
            FastApiIntegration(
                transaction_style="endpoint",
                failed_request_status_codes={403, *range(500, 599)},
                http_methods_to_capture=("DELETE", "GET", "PATCH", "POST", "PUT"),
            ),
        ],
    )


app = FastAPI(
    title=configs.project_name,
    description="",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc",
    openapi_tags=tags_metadata,
    default_response_class=ORJSONResponse,
    responses=responses,
    lifespan=lifespan,
)


@app.get("/sentry-debug")
async def trigger_error() -> None:
    _ = 1 / 0


@app.get("/main")
async def main() -> dict[str, str]:
    return {"message": "Email confirmed, say hello to main page!"}


app.add_middleware(TokenBucketMiddleware)  # pyright: ignore[reportArgumentType, reportCallIssue]

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


@app.exception_handler(ResponseError)
async def misdirected_error_handler(request: Request, exc: ResponseError) -> JSONResponse:  # noqa: RUF029
    return JSONResponse(status_code=status.HTTP_421_MISDIRECTED_REQUEST, content=exc.message.model_dump())


@app.exception_handler(AuthJWTException)
async def authjwt_exception_handler(request: Request, exc: AuthJWTException) -> JSONResponse:  # noqa: RUF029
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(access_control.router, prefix="/api/v1/access_control", dependencies=[Depends(get_jwt_user_global)])
app.include_router(oauth.router, prefix="/api/v1/oauth", tags=["OAuth"])
