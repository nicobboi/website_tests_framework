#! /usr/bin/env bash
set -e

python /app/app/celeryworker_pre_start.py

# SCHEDULER
celery -A app.worker beat -S celery_sqlalchemy_scheduler.schedulers:DatabaseScheduler -l info --detach

# WORKER
celery -A app.worker worker -l info -Q main-queue --pool prefork -c 5
