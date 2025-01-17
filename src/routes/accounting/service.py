from src import accounting
from src.models import Account, Transfer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, select, func, ScalarResult

from src.routes.transfers.service import options_transfers


async def create_account(session: AsyncSession, name: str, normal: int, currency: str) -> Account:
    account = accounting.create_account(session, name, normal, currency)
    await session.commit()
    return account


def filter_accounts(
    query: Select, normal: int | None = None, currency: str | None = None
) -> Select:
    if normal is not None:
        query = query.filter_by(normal=normal)

    if currency is not None:
        query = query.filter_by(currency=currency)

    return query


def options_accounts(query: Select) -> Select:
    return query


async def count_accounts(
    session: AsyncSession, normal: int | None = None, currency: str | None = None
) -> int:
    return await session.scalar(
        filter_accounts(select(func.count(Account.id)), normal=normal, currency=currency)
    )


async def list_accounts(
    session: AsyncSession,
    offset: int,
    limit: int,
    normal: int | None = None,
    currency: str | None = None,
) -> ScalarResult[Account]:
    return await session.scalars(
        options_accounts(
            filter_accounts(
                select(Account).offset(offset).limit(limit), normal=normal, currency=currency
            )
        )
    )


async def count_transfers(session: AsyncSession, account_id: int) -> int:
    return await session.scalar(select(func.count(Transfer.id)).filter_by(account_id=account_id))


async def list_transfers(session: AsyncSession, account_id: int, offset: int, limit: int):
    return await session.scalars(
        options_transfers(
            select(Transfer).filter_by(account_id=account_id).offset(offset).limit(limit)
        )
    )
