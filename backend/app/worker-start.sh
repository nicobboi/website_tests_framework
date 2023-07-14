#! /usr/bin/env bash
set -e

python /app/app/celeryworker_pre_start.py

# SCHEDULER
celery -A app.worker beat -S redisbeat.RedisScheduler -l info --detach

# WORKER
celery -A app.worker worker -l info -Q main-queue --pool prefork -c 5
