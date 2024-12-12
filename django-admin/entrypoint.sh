#!/bin/bash
set -eo pipefail +x

celery multi start w1 -A config -l INFO;
celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach;

python manage.py collectstatic --no-input
gunicorn --bind 0:8000 --log-level debug --max-requests 100 -w 16 config.wsgi:application
