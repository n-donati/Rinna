#!/bin/bash

# Set default port if not provided
export PORT=${PORT:-8000}

python manage.py collectstatic --noinput
python manage.py migrate

# Add SSL and error handling settings
gunicorn rinna.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 2 \
    --timeout 120 \
    --backlog 2048 \
    --max-requests 5000 \
    --max-requests-jitter 500 \
    --log-level debug \
    --capture-output \
    --enable-stdio-inheritance \
    --ssl-version TLSv1_2