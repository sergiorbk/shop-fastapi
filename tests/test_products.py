from decimal import Decimal
from uuid import UUID

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_product(client: AsyncClient):
    response = await client.post(
        "/v1/products",
        json={"name": "Test Product", "price": 99.99, "quantity": 10},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["kind"] == "ecommerce#product"
    assert data["item"]["name"] == "Test Product"
    assert Decimal(data["item"]["price"]) == Decimal("99.99")
    assert data["item"]["quantity"] == 10
    UUID(data["item"]["id"])


@pytest.mark.asyncio
async def test_get_product_by_id(client: AsyncClient):
    create_response = await client.post(
        "/v1/products",
        json={"name": "Single Product", "price": 50.00, "quantity": 1},
    )
    product_id = create_response.json()["item"]["id"]

    response = await client.get(f"/v1/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["kind"] == "ecommerce#product"
    assert data["item"]["name"] == "Single Product"
    assert Decimal(data["item"]["price"]) == Decimal("50.00")


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient):
    response = await client.get("/v1/products/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == 404
    assert data["error"]["status"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_update_product(client: AsyncClient):
    create_response = await client.post(
        "/v1/products",
        json={"name": "Old Name", "price": 10.00, "quantity": 5},
    )
    product_id = create_response.json()["item"]["id"]

    response = await client.put(
        f"/v1/products/{product_id}",
        json={"name": "New Name", "price": 15.00},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["kind"] == "ecommerce#product"
    assert data["item"]["name"] == "New Name"
    assert Decimal(data["item"]["price"]) == Decimal("15.00")
    assert data["item"]["quantity"] == 5


@pytest.mark.asyncio
async def test_update_product_not_found(client: AsyncClient):
    response = await client.put(
        "/v1/products/00000000-0000-0000-0000-000000000000",
        json={"name": "Updated"},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["status"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient):
    create_response = await client.post(
        "/v1/products",
        json={"name": "To Delete", "price": 10.00, "quantity": 1},
    )
    product_id = create_response.json()["item"]["id"]

    response = await client.delete(f"/v1/products/{product_id}")
    assert response.status_code == 204

    get_response = await client.get(f"/v1/products/{product_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_product_not_found(client: AsyncClient):
    response = await client.delete("/v1/products/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["status"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_validation_error(client: AsyncClient):
    response = await client.post(
        "/v1/products",
        json={"name": "Test"},
    )
    assert response.status_code == 422
    data = response.json()
    assert data["error"]["status"] == "INVALID_ARGUMENT"
    assert data["error"]["details"] is not None


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
