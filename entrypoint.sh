#!/usr/bin/env sh
set -e

cd /project/wallet_api

python manage.py migrate --noinput

exec gunicorn wallet_api.wsgi:application --bind 0.0.0.0:8000
