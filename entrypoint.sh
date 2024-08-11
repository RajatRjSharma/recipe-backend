#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Starting the server..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000
