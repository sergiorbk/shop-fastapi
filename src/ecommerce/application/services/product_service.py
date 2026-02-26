from uuid import UUID

from src.ecommerce.domain.entities.product import Product
from src.ecommerce.domain.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository):
        self._repository = repository

    async def get_product(self, product_id: UUID) -> Product | None:
        return await self._repository.get_by_id(product_id)

    async def create_product(self, product: Product) -> Product:
        return await self._repository.create(product)

    async def update_product(self, product_id: UUID, **kwargs) -> Product | None:
        existing = await self._repository.get_by_id(product_id)
        if not existing:
            return None

        for key, value in kwargs.items():
            if value is not None:
                setattr(existing, key, value)

        return await self._repository.update(existing)

    async def delete_product(self, product_id: UUID) -> bool:
        return await self._repository.delete(product_id)
