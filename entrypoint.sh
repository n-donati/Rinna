#!/bin/bash

# Set default port if not provided
export PORT=${PORT:-8000}

python manage.py collectstatic --noinput
python manage.py migrate

# Add workers and timeout settings
gunicorn rinna.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 2 \
    --timeout 60 \
    --log-level debug