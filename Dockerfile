# ─── base stage ───────────────────────────────────────────────────────────────
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_NO_CACHE=1 \
    # letakkan .venv di luar /app agar tidak tertimpa volume mount
    UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /app

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# copy dependency files only (layer cache)
COPY pyproject.toml uv.lock ./

# ─── dev stage ────────────────────────────────────────────────────────────────
FROM base AS dev

# install all deps
RUN uv sync --frozen

# /opt/venv aman dari volume mount .:/app
ENV PATH="/opt/venv/bin:$PATH"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ─── prod stage ───────────────────────────────────────────────────────────────
FROM base AS prod

# install deps tanpa dev extras
RUN uv sync --frozen --no-dev

COPY . .

ENV PATH="/opt/venv/bin:$PATH"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
