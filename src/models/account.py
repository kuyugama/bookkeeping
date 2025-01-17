from decimal import Decimal

from sqlalchemy import orm, CheckConstraint, String, Numeric

from .base import Base


class Account(Base, table="service_accounts"):
    __table_args__ = (
        CheckConstraint("normal IN (1, -1)", name="check_normal_positive_or_negative"),
    )
    name: orm.Mapped[255] = orm.mapped_column(String(255), unique=True, index=True)
    normal: orm.Mapped[int]

    currency: orm.Mapped[str] = orm.mapped_column(String(255), index=True)

    balance: orm.Mapped[Decimal] = orm.mapped_column(Numeric(28, 8), default=0, index=True)
