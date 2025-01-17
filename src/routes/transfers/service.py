from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src import accounting, constants
from src.models import Transfer, Account


def options_transfers(query: Select) -> Select:
    return query.options(joinedload(Transfer.account), joinedload(Transfer.transaction))


async def deposit_to_account(session: AsyncSession, account: Account, amount: float) -> Transfer:
    account_system = await accounting.get_or_create_account(
        session,
        f"{constants.ACCOUNT_SYSTEM}_{account.currency}",
        constants.CREDIT,
        account.currency,
    )

    transfer = accounting.make_transaction(
        session, constants.TRANSACTION_DEPOSIT, amount, account.currency, account_system, account
    )

    await session.commit()

    return transfer
