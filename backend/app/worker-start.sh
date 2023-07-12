#! /usr/bin/env bash
set -e

python /app/app/celeryworker_pre_start.py

# celery -A app.worker beat -l info --detach

celery -A app.worker worker -l info -Q main-queue --pool prefork -c 5
