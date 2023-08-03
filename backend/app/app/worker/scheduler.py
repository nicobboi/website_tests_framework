# from . import test_website, test_celery
from redisbeat.scheduler import RedisScheduler
from app.core.celery_app import celery_app
from datetime import datetime, timedelta
from pydantic import UUID4


def add_schedule(url: str, test_types: list[str], crontab_info: str, schedule_id: UUID4):
    """
    Schedule the periodic test to do on the given url
    """
    # example crontab string: "*, *, *, *, *"
    crontab_list = crontab_info.split(", ")

    print(schedule_id)

    scheduler = RedisScheduler(app=celery_app)
    for test_type in test_types:
        scheduler.add(**{
            'name': str(schedule_id),
            'task': 'tasks.test_website',
            'schedule': timedelta(minutes=1),
            'args': (url, test_type)
        })

        # print(str(scheduler.remove(str(schedule_id))))
    
    return "Schedule added correctly."

def remove_schedule(schedule_id: UUID4):
    """
    Remove a scheduled 
    """
    scheduler = RedisScheduler(app=celery_app)
    