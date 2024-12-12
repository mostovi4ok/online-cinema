#!/bin/bash
alembic upgrade head

set -eo pipefail +x
fastapi run main.py --reload
