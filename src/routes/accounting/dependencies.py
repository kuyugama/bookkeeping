from . import errors
from src.util import api_errors
from src import accounting, constants
from fastapi import Depends, Query, Path
from src.session_holder import acquire_session
from sqlalchemy.ext.asyncio import AsyncSession


@api_errors(errors.already_exist)
async def validate_account_create(
    name: str = Query(description="Назва рахунку"), session: AsyncSession = Depends(acquire_session)
):
    if name in constants.RESERVED_ACCOUNTS:
        raise errors.reserved

    account = await accounting.get_account(session, name)

    if account is not None:
        raise errors.already_exist


@api_errors(errors.not_found)
async def require_account(
    account_name: str = Path(description="Назва рахунку"),
    session: AsyncSession = Depends(acquire_session),
):
    account = await accounting.get_account(session, account_name)

    if account is None:
        raise errors.not_found

    return account
