from fastapi import APIRouter, Depends, Response
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.ecommerce.infrastructure.database import get_session
from src.ecommerce.infrastructure.logging import logger

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check(
    session: AsyncSession = Depends(get_session),
) -> Response:
    try:
        await session.execute(text("SELECT 1"))
        logger.info("Health check passed")
        return Response(status_code=200, content="OK")
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return Response(status_code=503, content="Service Unavailable")
