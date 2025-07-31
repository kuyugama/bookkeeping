from pydantic import Field

from .model import Object
from .account import Account


class Transfer(Object):
    amount: float = Field(description="Сума переказу")

    account: Account = Field(description="Рахунок переказу")
