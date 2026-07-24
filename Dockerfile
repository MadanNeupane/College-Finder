# =============================================================================
# College Finder — Dockerfile
# =============================================================================
# Multi-stage build:
#   builder   — installs Python dependencies (includes build tools)
#   runtime   — lean final image with no build tools
#
# Build args:
#   PYTHON_VERSION  Python image tag to use (default: 3.11-slim)
#   PORT            Port gunicorn listens on inside the container (default: 8000)
#   WORKERS         Gunicorn worker count (default: 2)
#
# The image works with SQLite (no extra services) or PostgreSQL
# (set DATABASE_URL env var). See docker-compose.yml for usage examples.
# =============================================================================

ARG PYTHON_VERSION=3.11-slim

# ---------------------------------------------------------------------------
# Stage 1 — builder: install Python deps
# ---------------------------------------------------------------------------
FROM python:${PYTHON_VERSION} AS builder

WORKDIR /app

# System packages needed to compile psycopg2, cryptography, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies into a virtual environment so they can be
# easily copied to the runtime stage.
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---------------------------------------------------------------------------
# Stage 2 — runtime: lean final image
# ---------------------------------------------------------------------------
FROM python:${PYTHON_VERSION} AS runtime

# Runtime-only system libraries (psycopg2 needs libpq at runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# --- Non-root user -----------------------------------------------------------
RUN groupadd --system appgroup && useradd --system --gid appgroup appuser

# --- Copy venv from builder --------------------------------------------------
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# --- Python env flags --------------------------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# --- App working directory ---------------------------------------------------
WORKDIR /app

# Copy project source
COPY . .

# Create writable directories for media & static output
RUN mkdir -p components/media staticfiles && \
    chown -R appuser:appgroup /app

# Switch to non-root before running anything
USER appuser

# --- Collect static files at build time -------------------------------------
# SECRET_KEY is set to a placeholder so collectstatic can run without a real
# secret. The real SECRET_KEY is injected at runtime via env / .env.
ARG PORT=8000
ARG WORKERS=2

RUN SECRET_KEY=build-placeholder \
    USE_WHITENOISE_MANIFEST=true \
    DATABASE_URL="" \
    python manage.py collectstatic --no-input --clear 2>/dev/null || \
    echo "WARNING: collectstatic failed — check STATICFILES_DIRS"

EXPOSE ${PORT}

# --- Entrypoint & default command -------------------------------------------
COPY --chown=appuser:appgroup docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

# Re-copy and fix permissions in case the COPY above changes ownership
USER root
RUN chmod +x /usr/local/bin/docker-entrypoint.sh && \
    chown appuser:appgroup /usr/local/bin/docker-entrypoint.sh
USER appuser

ENTRYPOINT ["docker-entrypoint.sh"]

# Override CMD via docker-compose or docker run to change workers / bind addr
CMD ["gunicorn", \
     "college_finder_app.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--threads", "2", \
     "--timeout", "120", \
     "--log-file", "-"]
