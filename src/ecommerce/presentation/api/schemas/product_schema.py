from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal
    quantity: int = 0


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    quantity: int | None = None


class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    price: Decimal
    quantity: int
