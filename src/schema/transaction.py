from .model import Object, Field


class Transaction(Object):
    category: str = Field(description="Категорія транзакції")
    currency: str = Field(description="Валюта транзакції")
