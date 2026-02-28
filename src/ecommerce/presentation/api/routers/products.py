from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.ecommerce.application.services.product_service import ProductService
from src.ecommerce.domain.entities.product import Product
from src.ecommerce.infrastructure.database import get_session
from src.ecommerce.infrastructure.database.repositories import SQLAlchemyProductRepository
from src.ecommerce.infrastructure.logging import logger
from src.ecommerce.presentation.api.schemas import (
    ErrorResponse,
    ItemResponse,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)

router = APIRouter(prefix="/v1/products", tags=["products"])

PRODUCT_KIND = "ecommerce#product"


def get_product_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    repository = SQLAlchemyProductRepository(session)
    return ProductService(repository)


def to_product_response(product: Product) -> ProductResponse:
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
    )


@router.get(
    "/{product_id}",
    response_model=ItemResponse[ProductResponse],
    responses={404: {"model": ErrorResponse}},
)
async def get_product(
    product_id: UUID,
    service: ProductService = Depends(get_product_service),
):
    product = await service.get_product(product_id)
    if not product:
        logger.warning(f"Product {product_id} not found")
        raise HTTPException(status_code=404, detail="Product not found")
    return ItemResponse(
        kind=PRODUCT_KIND,
        item=to_product_response(product),
    )


@router.post(
    "",
    response_model=ItemResponse[ProductResponse],
    status_code=201,
    responses={422: {"model": ErrorResponse}},
)
async def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    product = Product(
        id=None,
        name=data.name,
        description=data.description,
        price=data.price,
        quantity=data.quantity,
    )
    created = await service.create_product(product)
    logger.info(f"Created product {created.id}: {created.name}")
    return ItemResponse(
        kind=PRODUCT_KIND,
        item=to_product_response(created),
    )


@router.put(
    "/{product_id}",
    response_model=ItemResponse[ProductResponse],
    responses={404: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
)
async def update_product(
    product_id: UUID,
    data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    update_data = data.model_dump(exclude_unset=True)
    product = await service.update_product(product_id, **update_data)
    if not product:
        logger.warning(f"Product {product_id} not found for update")
        raise HTTPException(status_code=404, detail="Product not found")
    logger.info(f"Updated product {product_id}")
    return ItemResponse(
        kind=PRODUCT_KIND,
        item=to_product_response(product),
    )


@router.delete(
    "/{product_id}",
    status_code=204,
    responses={404: {"model": ErrorResponse}},
)
async def delete_product(
    product_id: UUID,
    service: ProductService = Depends(get_product_service),
):
    deleted = await service.delete_product(product_id)
    if not deleted:
        logger.warning(f"Product {product_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Product not found")
    logger.info(f"Deleted product {product_id}")
