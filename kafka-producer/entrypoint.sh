#!/bin/bash
set -eo pipefail +x

gunicorn wsgi_app:app --workers 4 --worker-class gevent --bind 0.0.0.0:5000 --log-level INFO
