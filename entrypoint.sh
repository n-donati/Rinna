#!/bin/bash

python manage.py collectstatic --noinput
python manage.py migrate
gunicorn rinna.wsgi:application --bind 0.0.0.0:$PORT