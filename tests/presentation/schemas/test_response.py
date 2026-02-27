from decimal import Decimal
from uuid import uuid4

from src.ecommerce.presentation.api.schemas import ItemResponse, ProductResponse


class TestItemResponse:
    def test_item_response(self):
        product_id = uuid4()
        product = ProductResponse(
            id=product_id,
            name="Test",
            description=None,
            price=Decimal("10.00"),
            quantity=1,
        )
        response = ItemResponse[ProductResponse](
            kind="ecommerce#product",
            item=product,
        )
        assert response.kind == "ecommerce#product"
        assert response.item.name == "Test"
