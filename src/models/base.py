from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncAttrs

from src.util import now


class Base(AsyncAttrs, orm.DeclarativeBase):

    def __init_subclass__(cls, **kwargs):
        if not hasattr(cls, "__tablename__") and "table" in kwargs:
            cls.__tablename__ = kwargs.pop("table")

        super().__init_subclass__(**kwargs)

    id: orm.Mapped[int] = orm.mapped_column(sa.BIGINT, primary_key=True, index=True)

    created_at: orm.Mapped[datetime] = orm.mapped_column(default=now, index=True)
    updated_at: orm.Mapped[datetime] = orm.mapped_column(
        default=None, nullable=True, onupdate=now, index=True
    )
