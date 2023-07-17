# from . import test_website, test_celery
from redisbeat.scheduler import RedisScheduler
from app.core.celery_app import celery_app
from datetime import datetime, timedelta


def schedule_tasks():
    scheduler = RedisScheduler(app=celery_app)
    scheduler.add(**{
        'name': 'test',
        'task': 'worker.tasks.test_celery',
        'schedule': timedelta(seconds=10),
        'args': ("Hello world!")
    })
    print("Aggiunto task!")