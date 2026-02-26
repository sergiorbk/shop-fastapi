from abc import ABC, abstractmethod
from uuid import UUID

from src.ecommerce.domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Product | None:
        pass

    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def update(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def delete(self, product_id: UUID) -> bool:
        pass
