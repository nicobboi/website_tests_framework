from datetime import timedelta
from app.core.celery_app import celery_app
from .redisbeat import RedisScheduler

from pydantic import BaseModel

class ScheduleInfo(BaseModel):
    """
    Validation class for schedule time info
    """
    min: int
    hour: int
    day: int

def add_schedule(url: str, schedule_name: str, test_type: str, schedule_time: ScheduleInfo):
    """
    Add new schedule (return True on success)
    """
    with RedisScheduler(app=celery_app) as scheduler:
        schedule_info = timedelta(
            minutes=schedule_time.min,
            hours=schedule_time.hour,
            days=schedule_time.day
        )

        # schedule configuration
        schedule = {
            'name': schedule_name,
            'task': 'app.worker.tasks.test_add',
            'schedule': schedule_info,
            'options': {'queue': 'main-queue'},
            'args': (url, test_type)
        }
        # add schedule to scheduler
        response = scheduler.add(**schedule)

    return response

def rem_schedule(schedule_name: str):
    """
    Remove a schedule by its name/identifier (return True if has been found, False else)
    """
    with RedisScheduler(app=celery_app) as scheduler:
        response = scheduler.remove(schedule_name)

    return response


def schedule_list():
    """
    Return the list of all the schedules currently operating
    """
    with RedisScheduler(app=celery_app) as scheduler:
        s_list = scheduler.list()

    return s_list