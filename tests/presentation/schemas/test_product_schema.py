from decimal import Decimal
from uuid import uuid4

from src.ecommerce.presentation.api.schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)


class TestProductCreate:
    def test_create_with_all_fields(self):
        data = ProductCreate(
            name="Test Product",
            description="Description",
            price=Decimal("99.99"),
            quantity=10,
        )
        assert data.name == "Test Product"
        assert data.price == Decimal("99.99")

    def test_create_with_defaults(self):
        data = ProductCreate(
            name="Test",
            price=Decimal("10.00"),
        )
        assert data.description is None
        assert data.quantity == 0


class TestProductUpdate:
    def test_partial_update(self):
        data = ProductUpdate(name="New Name")
        dump = data.model_dump(exclude_unset=True)
        assert dump == {"name": "New Name"}

    def test_full_update(self):
        data = ProductUpdate(
            name="New Name",
            description="New Desc",
            price=Decimal("50.00"),
            quantity=5,
        )
        dump = data.model_dump(exclude_unset=True)
        assert len(dump) == 4


class TestProductResponse:
    def test_response(self):
        product_id = uuid4()
        response = ProductResponse(
            id=product_id,
            name="Test",
            description=None,
            price=Decimal("50.00"),
            quantity=5,
        )
        assert response.id == product_id
        assert response.name == "Test"
