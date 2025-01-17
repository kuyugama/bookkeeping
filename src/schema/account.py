from typing import Literal
from .model import Object, Field


class Account(Object):
    name: str = Field(description="Назва рахунку")
    normal: Literal[1, -1] = Field(description="Тип рахунку (-1 кредит, 1 дебет)")

    currency: str = Field(description="Валюта рахунку")
    balance: float = Field(description="Баланс рахунку")
