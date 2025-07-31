from typing import Annotated
from datetime import datetime, timedelta

from pydantic import BaseModel, ConfigDict, PlainSerializer, Field

from src.util.datetime_util import utc_timestamp


datetime_pd = Annotated[
    datetime,
    PlainSerializer(
        lambda x: x and int(utc_timestamp(x)),
        return_type=int,
    ),
]

timedelta_pd = Annotated[
    timedelta,
    PlainSerializer(
        lambda x: int(x.total_seconds()),
        return_type=int,
    ),
]


class Schema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True,
        validate_default=True,
    )


class Object(Schema):
    id: int

    created: datetime_pd = Field(
        description="Дата та час створення об'єкту", validation_alias="created_at"
    )
    updated: datetime_pd | None = Field(
        None, description="Дата та час останнього оновлення об'єкту", validation_alias="updated_at"
    )
