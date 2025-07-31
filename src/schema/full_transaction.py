from pydantic import Field
from .transfer import Transfer
from .transaction import Transaction


class FullTransaction(Transaction):
    input_transfers: list[Transfer] = Field(description="Вхідні перекази")
    output_transfers: list[Transfer] = Field(description="Вихідні перекази")
