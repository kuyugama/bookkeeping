from .account import Account
from .model import Object, Field
from .transaction import Transaction


class Transfer(Object):
    amount: float = Field(description="Сума переведення")

    account: Account = Field(description="Рахунок переведення")
    transaction: Transaction = Field(description="Транзакція переведення")
