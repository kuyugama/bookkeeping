from pydantic import Field

from .model import Object


class Transaction(Object):
    category: str = Field(description="Категорія транзакції")
    currency: str = Field(description="Валюта транзакції")
