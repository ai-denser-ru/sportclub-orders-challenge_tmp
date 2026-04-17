# Stage 1: Build and Test
FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies including dev (pytest)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --all-extras

# Copy application code
COPY . .

# Run tests; build fails if tests fail
RUN uv run pytest

# Stage 2: Production
FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy the environment and application from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app /app/app
# We could also copy seed.py if we need to run it, but assuming it's in /app/app/seed.py
COPY --from=builder /app/pyproject.toml /app/pyproject.toml

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
