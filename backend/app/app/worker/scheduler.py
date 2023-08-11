from celery.schedules import crontab
from app.core.celery_app import celery_app
from .redisbeat import RedisScheduler

from pydantic import BaseModel

class ScheduleInfo(BaseModel):
    """
    Validation class for schedule time info
    """
    min: int
    hour: int
    days: list[str]

def intFromDay(days: list[str]) -> list[int]:
    """
    Return a list of integer from days name (for crontab 'day_of_week' attribute)
    """
    output = []
    for day in days:
        if day == "sunday": output.append(0)
        if day == "monday": output.append(1)
        if day == "tuesday": output.append(2)
        if day == "wednesday": output.append(3)
        if day == "thursday": output.append(4)
        if day == "friday": output.append(5)
        if day == "saturday": output.append(6)

    return output


def add_schedule(url: str, schedule_name: str, test_type: str, schedule_time: ScheduleInfo):
    """
    Add new schedule (return True on success)
    """
    scheduler = RedisScheduler(app=celery_app)
    schedule_info = crontab(
        minute=[schedule_time.min],
        hour=[schedule_time.hour],
        day_of_week=intFromDay(schedule_time.days)
    )

    # schedule configuration
    schedule = {
        'name': schedule_name,
        'task': 'app.worker.tasks.test_website',
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
    scheduler = RedisScheduler(app=celery_app)
    response = scheduler.remove(schedule_name)

    return response


def schedule_list():
    """
    Return the list of all the schedules currently operating
    """
    scheduler = RedisScheduler(app=celery_app)
    s_list = scheduler.list()

    return s_list