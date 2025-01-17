from . import typing_util

from .pydantic_util import format_error

from .string_util import snake_to_camel

from .fastapi_util import api_errors, setup_route_errors

from .datetime_util import now, utc_timestamp, from_utc_timestamp


__all__ = [
    # ============ Typing Utils ============
    "typing_util",
    # ============ Pydantic Utils ============
    "format_error",
    # ============ String Utils ============
    "snake_to_camel",
    # ============ FastAPI Utils ============
    "api_errors",
    "setup_route_errors",
    # ============ Datetime Utils ============
    "now",
    "utc_timestamp",
    "from_utc_timestamp",
    # ============ Miscellaneous Utils ============
    "get_offset_and_limit",
    "paginated_response",
]


import math
import typing
from src import constants
from sqlalchemy.orm import DeclarativeBase


def get_offset_and_limit(page: int, size: int = constants.DEFAULT_PAGE_SIZE):
    return (page - 1) * size, size


def paginated_response(
    items: typing.Sequence[DeclarativeBase],
    total: int,
    page: int,
    limit: int,
):
    return {
        "items": items,
        "pagination": {
            "total": total,
            "page": page,
            "pages": math.ceil(total / limit),
        },
    }
