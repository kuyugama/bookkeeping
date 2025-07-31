from typing import Never
from src import constants
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Account, Transaction, Transfer


def create_account(session: AsyncSession, name: str, normal: int, currency: str) -> Account:
    """
    Creates a new account, BUT not commits changes
    """
    if normal not in (constants.DEBIT, constants.CREDIT):
        raise ValueError("normal must be either -1 or 1")

    account = Account(
        name=name,
        normal=normal,
        currency=currency,
    )

    session.add(account)

    return account


async def get_account(session: AsyncSession, name: str) -> Account | None:
    """
    Gets an account by name
    """
    return await session.scalar(select(Account).filter_by(name=name))


async def get_or_create_account(
    session: AsyncSession, name: str, normal: int, currency: str
) -> Account:
    """
    Ensure that an account exists in database before returning
    """
    account = await get_account(session, name)

    if account is None:
        account = create_account(session, name, normal, currency)
        await session.commit()

    return account


def make_transaction(
    session: AsyncSession,
    category: str,
    amount: float | Decimal,
    currency: str,
    from_account: Account,
    to_account: Account,
) -> Never | Transfer:
    """
    Makes a transaction of ``category`` between ``from_account`` and ``to_account`` in ``currency`` with ``amount``.
    BUT not commits changes.

    Returns a ``Transfer`` object for ``to_account``
    """
    if currency != from_account.currency or currency != to_account.currency:
        raise ValueError(
            f"Currency not matches account's currencies: {currency} != {from_account.currency} != {to_account.currency}"
        )

    transaction = Transaction(
        category=category,
        currency=currency,
    )

    transfer_from = Transfer(
        amount=amount * constants.CREDIT,
        account=from_account,
        transaction=transaction,
    )

    transfer_to = Transfer(
        amount=amount * constants.DEBIT,
        account=to_account,
        transaction=transaction,
    )

    transaction.transfers.extend([transfer_from, transfer_to])

    session.add_all([transaction])

    return transfer_to
