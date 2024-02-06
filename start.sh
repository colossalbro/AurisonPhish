#!/bin/bash

python manage.py makemigrations mails
python manage.py makemigrations management
python manage.py makemigrations core
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py scheduler &  # Run in the background
gunicorn core.wsgi:application --bind 0.0.0.0:8000

