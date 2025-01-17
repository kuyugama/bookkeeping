from .model import Schema, Field
from typing import Generic, TypeVar


__all__ = ["Paginated"]


class PaginationData(Schema):
    total: int = Field(ge=0, description="Загальна кількість об'єктів")
    page: int = Field(ge=1, description="№ сторінки")
    pages: int = Field(ge=0, description="Загальна кількість сторінок")


T_s = TypeVar("T_s", bound=Schema)


class Paginated(Schema, Generic[T_s]):
    pagination: PaginationData = Field(description="Інформація про кількість об'єктів та сторінок")
    items: list[T_s] = Field(description="Список об'єктів")
