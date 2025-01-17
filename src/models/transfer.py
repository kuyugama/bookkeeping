from .base import Base
from decimal import Decimal
from .account import Account
from .transaction import Transaction
from sqlalchemy import orm, Numeric, ForeignKey, event, Connection, update


class Transfer(Base, table="service_transfers"):
    amount: orm.Mapped[Decimal] = orm.mapped_column(Numeric(28, 8))

    account_id = orm.mapped_column(ForeignKey(Account.id, ondelete="CASCADE"))
    account: orm.Mapped[Account] = orm.relationship(foreign_keys=[account_id])

    transaction_id = orm.mapped_column(ForeignKey(Transaction.id, ondelete="CASCADE"))
    transaction: orm.Mapped[Transaction] = orm.relationship(foreign_keys=[transaction_id])


@event.listens_for(Transfer, "before_insert")
def _new_transfer(_: type[Transfer], connection: Connection, transfer: Transfer):
    account = transfer.account

    connection.execute(
        update(Account)
        .values(balance=Account.balance + transfer.amount * account.normal)
        .filter_by(id=account.id)
    )
    account.balance += Decimal(transfer.amount * account.normal)


@event.listens_for(Transfer, "before_delete")
def _remove_transfer(_: type[Transfer], connection: Connection, transfer: Transfer):
    account = transfer.account
    connection.execute(
        update(Account)
        .values(balance=Account.balance - transfer.amount * account.normal)
        .filter_by(id=account.id)
    )
    account.balance -= Decimal(transfer.amount * account.normal)
