import sys
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.ecommerce.infrastructure.database import Base, get_session
from src.ecommerce.infrastructure.database.models import ProductModel  # noqa: F401
from src.ecommerce.presentation.api.app import app

if sys.platform == "win32":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class TestSettings(BaseSettings):
    test_db_host: str = "localhost"
    test_db_port: int = 5432
    test_db_name: str = "shop_test"
    test_db_user: str = "postgres"
    test_db_password: str = "postgres"

    model_config = {"env_file": ".env", "extra": "ignore"}


test_settings = TestSettings()

TEST_DATABASE_URL = f"postgresql+asyncpg://{test_settings.test_db_user}:{test_settings.test_db_password}@{test_settings.test_db_host}:{test_settings.test_db_port}/{test_settings.test_db_name}"


@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()
