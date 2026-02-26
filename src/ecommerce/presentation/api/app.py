import asyncio
import signal
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.ecommerce.infrastructure.database import engine
from src.ecommerce.infrastructure.logging import logger
from src.ecommerce.presentation.api.exceptions import register_exception_handlers
from src.ecommerce.presentation.api.routers import health, products


def run_migrations() -> None:
    import subprocess

    result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Migration failed: {result.stderr}")
    else:
        logger.info("Database migrations completed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    run_migrations()

    original_sigterm = signal.getsignal(signal.SIGTERM)
    original_sigint = signal.getsignal(signal.SIGINT)

    def handle_signal(signum, frame):
        logger.info("SIGTERM received. Starting graceful shutdown...")
        if signum == signal.SIGTERM and callable(original_sigterm):
            original_sigterm(signum, frame)
        elif signum == signal.SIGINT and callable(original_sigint):
            original_sigint(signum, frame)

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    yield

    logger.info("Closing database connections")
    await engine.dispose()
    logger.info("Application shutdown complete")


app = FastAPI(
    title="E-Commerce API",
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(health.router)
app.include_router(products.router)
