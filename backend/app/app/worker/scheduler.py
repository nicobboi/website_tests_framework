from celery.schedules import crontab
from app.core.celery_app import celery_app
from .redisbeat import RedisScheduler
from datetime import time

from sqlalchemy.orm import Session

from app import crud

from pydantic import BaseModel

class ScheduleInfo(BaseModel):
    """
    Validation class for schedule time info
    """
    time_info: time
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


def init_scheduler(db: Session) -> None:
    """
    Insert initial data into celery scheduler
    """
    active_schedules = crud.schedule.get_all(db=db, active=True)
    if not active_schedules: return

    schedule_in_scheduler = schedule_list()

    for schedule in active_schedules:
        if schedule in [ss.name for ss in schedule_in_scheduler]: continue
        add_schedule(
            url=schedule.url,
            schedule_name=str(schedule.id),
            test_type=schedule.test_type,
            schedule_time=ScheduleInfo(
                time_info=schedule.schedule_info.time_info,
                days=schedule.schedule_info.days
            )
        )

def add_schedule(url: str, schedule_name: str, test_type: str, schedule_time: ScheduleInfo):
    """
    Add new schedule (return True on success)
    """
    scheduler = RedisScheduler(app=celery_app)
    schedule_info = crontab(
        minute=str(schedule_time.time_info.minute),
        hour=str(schedule_time.time_info.hour),
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
    return scheduler.list()