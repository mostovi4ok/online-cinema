#!/bin/bash
set -eo pipefail +x

docker exec Tests bash -c 'bash wait_for_services.sh'
docker exec Tests bash -c 'python -m pytest'
