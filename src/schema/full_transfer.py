from pydantic import Field

from .transfer import Transfer
from .transaction import Transaction


class FullTransfer(Transfer):
    transaction: Transaction = Field(description="Транзакція переведення")
