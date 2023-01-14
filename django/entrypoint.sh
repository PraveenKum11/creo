#!/bin/sh

cd /usr/src/django_app
# python manage.py migrate --no-input
# python manage.py collectstatic --no-input

gunicorn setup.wsgi:application --bind 0.0.0.0:8000