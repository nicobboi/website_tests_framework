from celery import Celery

celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.timezone = "Europe/Rome"

celery_app.conf.task_routes = {"app.worker.*": "main-queue"}

# celery_app.conf.beat_dburi = 'sqlite:///app/worker/schedule.db'
