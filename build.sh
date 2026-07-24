#!/usr/bin/env bash
# =============================================================================
# build.sh — Render.com build script
# =============================================================================
# Called by Render before starting the web service.
# NOTE: makemigrations is intentionally NOT run here — migrations should be
#       committed to the repository, not auto-generated in CI/CD.
set -o errexit

echo "==> Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Applying database migrations..."
python manage.py migrate --no-input

echo "==> Loading fixture data (if any)..."
python populate_fixtures.py || echo "No fixture data to load (skipping)."

echo "==> Build complete."
