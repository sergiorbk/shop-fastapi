# Dockerfile for ecommerce application by Serhii Rybak 2026

# =============================================================
# STAGE 1: Builder (lightweight image, venv setup)
# =============================================================
FROM python:3.13.9-slim AS builder

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# copy dependency file
COPY pyproject.toml uv.lock ./

# create venv and install dependencies from lock file (no version updates, no dev dependencies, dependencies only)
RUN uv sync --frozen --no-dev --no-install-project

# =============================================================
# STAGE 2: Final (Runtime)
# =============================================================
FROM python:3.13.9-slim as final
WORKDIR /app

# copy ready venv from builder stage
COPY --from=builder /app/.venv /app/.venv

# add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# copy app code and db migrations
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# setup a port
EXPOSE 8080

# start fastapi app
CMD ["uvicorn", "src.ecommerce.presentation.api.app:app", "--host", "0.0.0.0", "--port", "8080"]