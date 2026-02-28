from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from src.ecommerce.domain.entities.product import Product
from src.ecommerce.domain.repositories.product_repository import ProductRepository
from src.ecommerce.infrastructure.database.models.product_model import ProductModel


class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_entity(self, model: ProductModel) -> Product:
        return Product(
            id=model.id,
            name=model.name,
            description=model.description,
            price=Decimal(str(model.price)),
            quantity=model.quantity,
        )

    def _to_model(self, entity: Product) -> ProductModel:
        return ProductModel(
            id=entity.id or uuid4(),
            name=entity.name,
            description=entity.description,
            price=float(entity.price),
            quantity=entity.quantity,
        )

    async def get_by_id(self, product_id: UUID) -> Product | None:
        model = await self._session.get(ProductModel, product_id)
        return self._to_entity(model) if model else None

    async def create(self, product: Product) -> Product:
        model = self._to_model(product)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def update(self, product: Product) -> Product:
        model = await self._session.get(ProductModel, product.id)
        if model:
            model.name = product.name
            model.description = product.description
            model.price = float(product.price)
            model.quantity = product.quantity
            await self._session.commit()
            await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, product_id: UUID) -> bool:
        model = await self._session.get(ProductModel, product_id)
        if not model:
            return False
        await self._session.delete(model)
        await self._session.commit()
        return True
