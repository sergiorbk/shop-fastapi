from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass
class Product:
    id: UUID | None
    name: str
    description: str | None
    price: Decimal
    quantity: int = 0

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
