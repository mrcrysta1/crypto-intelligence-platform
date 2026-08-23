# syntax=docker/dockerfile:1.4
# ============================================================
# Crypto Intelligence Platform - API
# Multi-stage build:
#   Stage 1 (base):       Python 3.12-slim + system deps
#   Stage 2 (builder):    install Python dependencies into venv
#   Stage 3 (development): dev tooling + hot reload
#   Stage 4 (runtime):    minimal non-root production image
# ============================================================

ARG PYTHON_VERSION=3.12

# ------------------------------------------------------------
# Stage 1: Base image with system dependencies
# ------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ------------------------------------------------------------
# Stage 2: Builder - install dependencies into isolated venv
# ------------------------------------------------------------
FROM base AS builder

COPY apps/api/requirements.txt /tmp/requirements.txt

RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip setuptools wheel \
    && /opt/venv/bin/pip install -r /tmp/requirements.txt

# ------------------------------------------------------------
# Stage 3: Development image - full toolchain + hot reload
# ------------------------------------------------------------
FROM base AS development

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY apps/api/requirements.txt /tmp/requirements.txt
COPY apps/api/requirements-dev.txt* /tmp/

RUN pip install --no-cache-dir debugpy watchdog || true; \
    if [ -f /tmp/requirements-dev.txt ]; then pip install --no-cache-dir -r /tmp/requirements-dev.txt; fi

COPY apps/api/ /app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ------------------------------------------------------------
# Stage 4: Production runtime - minimal, non-root, healthchecked
# ------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 1000 crypto \
    && useradd --uid 1000 --gid crypto --shell /bin/bash --create-home crypto

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY --chown=crypto:crypto apps/api/ /app/

USER crypto

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
