#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Load fixture data
python manage.py populate_fixtures || echo "No fixture data to load"

