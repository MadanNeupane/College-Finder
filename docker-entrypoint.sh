#!/bin/sh
# =============================================================================
# Docker Entrypoint — runs before the main process starts
# =============================================================================
set -e

echo "==> Running database migrations..."
python manage.py migrate --no-input

echo "==> Creating superuser (if credentials are set)..."
python create_superuser.py || echo "Superuser step skipped."

echo "==> Starting application..."
exec "$@"
