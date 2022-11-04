#!/bin/sh
python manage.py migrate --no-input
gunicorn src.wsgi --reload --bind 0.0.0.0:8000