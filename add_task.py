#!/usr/bin/env python
# encoding: utf-8
from datetime import timedelta

from redisbeat.scheduler import RedisScheduler

# from tasks import app
# from app import worker as app
from app.core.celery_app import celery_app as app

###




if __name__ == "__main__":
    schduler = RedisScheduler(app=app)
    import pdb; pdb.set_trace()
    schduler.add(**{
        'name': 'sub-perminute',
        'task': 'app.worker.tests.test_celery',
        'schedule': timedelta(seconds=3),
        'args': ("hello")
    })

