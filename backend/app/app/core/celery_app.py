from celery import Celery

# celery app configuration
celery_app = Celery('worker')
celery_app.conf.broker_url = 'redis://redis:6379/0'
celery_app.conf.result_backend = 'redis://redis:6379/0'

celery_app.conf.update(
    CELERY_REDIS_SCHEDULER_URL = 'redis://redis:6379',
    beat_schedule = {}
)

celery_app.conf.timezone = "Europe/Rome"

celery_app.conf.task_routes = {"app.worker.*": "main-queue"}


