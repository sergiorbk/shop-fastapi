from uuid import UUID, uuid4

from sqlalchemy import Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from src.ecommerce.infrastructure.database.connection import Base


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(default=0)
