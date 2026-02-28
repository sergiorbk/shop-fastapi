from decimal import Decimal
from uuid import uuid4

import pytest

from src.ecommerce.domain.entities.product import Product


class TestProduct:
    def test_create_product(self):
        product = Product(
            id=uuid4(),
            name="Test Product",
            description="Description",
            price=Decimal("99.99"),
            quantity=10,
        )
        assert product.name == "Test Product"
        assert product.price == Decimal("99.99")
        assert product.quantity == 10

    def test_create_product_without_id(self):
        product = Product(
            id=None,
            name="New Product",
            description=None,
            price=Decimal("50.00"),
        )
        assert product.id is None
        assert product.quantity == 0

    def test_product_negative_price_raises_error(self):
        with pytest.raises(ValueError, match="Price cannot be negative"):
            Product(
                id=None,
                name="Invalid",
                description=None,
                price=Decimal("-10.00"),
            )

    def test_product_negative_quantity_raises_error(self):
        with pytest.raises(ValueError, match="Quantity cannot be negative"):
            Product(
                id=None,
                name="Invalid",
                description=None,
                price=Decimal("10.00"),
                quantity=-5,
            )

    def test_product_zero_price_allowed(self):
        product = Product(
            id=None,
            name="Free Product",
            description=None,
            price=Decimal("0.00"),
        )
        assert product.price == Decimal("0.00")
