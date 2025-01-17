from src import util, constants
from . import service
from src import schema
from typing import Literal
from fastapi import APIRouter, Depends
from ..dependencies import require_page
from src.session_holder import acquire_session
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies import validate_account_create, require_account
from ..transfers.service import deposit_to_account
from ...models import Account

router = APIRouter(prefix="/accounting", tags=["Рахунки"])


@router.post(
    "/",
    summary="Створити рахунок",
    response_model=schema.Account,
    operation_id="create_account",
    dependencies=[Depends(validate_account_create)],
)
async def create_account(
    name: str,
    currency: str,
    session: AsyncSession = Depends(acquire_session),
):
    return await service.create_account(session, name, constants.DEBIT, currency)


@router.get(
    "/",
    summary="Отримати список рахунків",
    response_model=schema.Paginated[schema.Account],
    operation_id="list_accounts",
)
async def list_accounts(
    page: int = Depends(require_page),
    session: AsyncSession = Depends(acquire_session),
):
    offset, limit = util.get_offset_and_limit(page)

    total = await service.count_accounts(session)
    items = await service.list_accounts(session, offset, limit)

    return util.paginated_response(items.all(), total, page, limit)


@router.get(
    "/{account_name}/transfers",
    summary="Отримати переведення рахунку",
    response_model=schema.Paginated[schema.Transfer],
    operation_id="list_transfers",
)
async def list_transfers(
    account: Account = Depends(require_account),
    page: int = Depends(require_page),
    session: AsyncSession = Depends(acquire_session),
):
    offset, limit = util.get_offset_and_limit(page)

    total = await service.count_transfers(session, account.id)
    items = await service.list_transfers(session, account.id, offset, limit)

    return util.paginated_response(items.all(), total, page, limit)


@router.post(
    "/{account_name}/deposit",
    summary="Поповнити рахунок",
    response_model=schema.Transfer,
    operation_id="deposit_to_account",
)
async def deposit(
    amount: float,
    account: Account = Depends(require_account),
    session: AsyncSession = Depends(acquire_session),
):
    return await deposit_to_account(session, account, amount)
