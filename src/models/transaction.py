import typing

from .base import Base
from sqlalchemy import orm
from sqlalchemy.util import hybridproperty


if typing.TYPE_CHECKING:
    from src.models import Transfer


class Transaction(Base, table="service_transactions"):
    category: orm.Mapped[str] = orm.mapped_column(index=True)
    currency: orm.Mapped[str] = orm.mapped_column(index=True)

    transfers: orm.Mapped[list["Transfer"]] = orm.relationship(
        back_populates="transaction"
    )

    @hybridproperty
    def input_transfers(self):
        return [t for t in self.transfers if t.amount > 0]

    @hybridproperty
    def output_transfers(self):
        return [t for t in self.transfers if t.amount < 0]
