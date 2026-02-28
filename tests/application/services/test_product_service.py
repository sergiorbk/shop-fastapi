from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.ecommerce.application.services.product_service import ProductService
from src.ecommerce.domain.entities.product import Product
from src.ecommerce.domain.repositories.product_repository import ProductRepository


@pytest.fixture
def mock_repository():
    return AsyncMock(spec=ProductRepository)


@pytest.fixture
def product_service(mock_repository):
    return ProductService(mock_repository)


@pytest.fixture
def sample_product():
    return Product(
        id=uuid4(),
        name="Test Product",
        description="Test Description",
        price=Decimal("99.99"),
        quantity=10,
    )


class TestProductService:
    @pytest.mark.asyncio
    async def test_get_product_found(self, product_service, mock_repository, sample_product):
        mock_repository.get_by_id.return_value = sample_product

        result = await product_service.get_product(sample_product.id)

        assert result == sample_product
        mock_repository.get_by_id.assert_called_once_with(sample_product.id)

    @pytest.mark.asyncio
    async def test_get_product_not_found(self, product_service, mock_repository):
        mock_repository.get_by_id.return_value = None
        product_id = uuid4()

        result = await product_service.get_product(product_id)

        assert result is None
        mock_repository.get_by_id.assert_called_once_with(product_id)

    @pytest.mark.asyncio
    async def test_create_product(self, product_service, mock_repository, sample_product):
        mock_repository.create.return_value = sample_product

        result = await product_service.create_product(sample_product)

        assert result == sample_product
        mock_repository.create.assert_called_once_with(sample_product)

    @pytest.mark.asyncio
    async def test_update_product_found(self, product_service, mock_repository, sample_product):
        mock_repository.get_by_id.return_value = sample_product
        updated_product = Product(
            id=sample_product.id,
            name="Updated Name",
            description=sample_product.description,
            price=sample_product.price,
            quantity=sample_product.quantity,
        )
        mock_repository.update.return_value = updated_product

        result = await product_service.update_product(sample_product.id, name="Updated Name")

        assert result.name == "Updated Name"
        mock_repository.get_by_id.assert_called_once()
        mock_repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_product_not_found(self, product_service, mock_repository):
        mock_repository.get_by_id.return_value = None
        product_id = uuid4()

        result = await product_service.update_product(product_id, name="New Name")

        assert result is None
        mock_repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_product_found(self, product_service, mock_repository):
        mock_repository.delete.return_value = True
        product_id = uuid4()

        result = await product_service.delete_product(product_id)

        assert result is True
        mock_repository.delete.assert_called_once_with(product_id)

    @pytest.mark.asyncio
    async def test_delete_product_not_found(self, product_service, mock_repository):
        mock_repository.delete.return_value = False
        product_id = uuid4()

        result = await product_service.delete_product(product_id)

        assert result is False
