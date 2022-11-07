#!/bin/sh
python manage.py migrate --no-input
celery -A src worker -l INFO --detach
gunicorn src.wsgi --reload --bind 0.0.0.0:8000