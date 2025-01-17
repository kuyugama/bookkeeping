import logging
from contextlib import asynccontextmanager
from typing import Callable, AsyncContextManager

import fastapi
from fastapi import APIRouter, FastAPI

import config
from src import schema, error
from src.error import APIError
from src.session_holder import session_holder
from src.routes import router as routes_router

from src.util import (
    format_error,
    setup_route_errors,
)

root_router = fastapi.APIRouter()
root_router.include_router(routes_router)


def error_handler(_, exc: APIError):
    return exc.response


endpoint_not_found = error.define_error("endpoint", "not-found", "Path {path} not found", 404)


async def default_handler(scope, receive, send):
    await endpoint_not_found(extra=scope).response(scope, receive, send)


async def validation_error_handler(
    _: fastapi.Request, exc: fastapi.exceptions.RequestValidationError
):
    formatted_error = format_error(exc)

    return fastapi.responses.JSONResponse(
        formatted_error,
        status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def create_lifespan(test_mode: bool = True) -> Callable[[FastAPI], AsyncContextManager[None]]:
    async def lifespan(app: fastapi.FastAPI):
        if test_mode:
            pass
        else:
            session_holder.init(url=config.settings.postgresql.url)
            setup_route_errors(app)

        yield

        if not test_mode:
            await session_holder.close()

    return asynccontextmanager(lifespan)


def make_app(test_mode: bool = False) -> fastapi.FastAPI:
    logging.basicConfig(level=logging.DEBUG)
    app = fastapi.FastAPI(
        lifespan=create_lifespan(test_mode=test_mode),
        redoc_url=None,
        responses={422: dict(model=schema.ValidationErrorModel)},
        title=config.settings.app.title,
        version=config.settings.app.version,
    )

    router: APIRouter = getattr(app, "router")
    router.default = default_handler

    app.include_router(root_router)

    app.exception_handler(error.APIError)(error_handler)
    app.exception_handler(fastapi.exceptions.RequestValidationError)(validation_error_handler)

    return app


@root_router.get(
    "/",
    response_class=fastapi.responses.RedirectResponse,
    include_in_schema=False,
)
async def root():
    return fastapi.responses.RedirectResponse(
        "/docs", status_code=fastapi.status.HTTP_308_PERMANENT_REDIRECT
    )


@root_router.get("/errors", summary="Отримати список всіх помилок", operation_id="list_errors")
async def _errors() -> dict[str, dict[str, tuple[str, int]]]:
    # noinspection PyProtectedMember
    return error.errors
