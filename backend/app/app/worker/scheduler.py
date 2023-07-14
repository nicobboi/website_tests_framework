# from app.core.celery_app import get_scheduler_db
# from . import test_website, test_celery
from redisbeat.scheduler import RedisScheduler
from datetime import datetime, timedelta


def schedule_tasks(scheduler_db=get_scheduler_db()):
    # create a crontab schedule
    schedule = CrontabSchedule(
        minute='*',
        hour='*',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
        timezone='Rome/Europe',
    )
    scheduler_db.add(schedule)
    try:
        scheduler_db.commit()
    except Exception as e:
        print("ERROR\t     Exception occurred on committing scheduled task: {}".format(str(e)))
        scheduler_db.close()
        return
    # create a periodic task
    periodic_task = PeriodicTask(
        crontab=schedule,
        name='Test',
        task='worker.tests.test_celery',
        kwargs=json.dumps({
            'word': 'Hello world!'
        }),
        expires=datetime.utcnow() + timedelta(minutes=3)
    )
    # and add to scheduler database
    scheduler_db.add(periodic_task)
    try:
        scheduler_db.commit()
    except Exception as e:
        print("ERROR\t     Exception occurred on committing scheduled task: {}".format(str(e)))
        scheduler_db.close()
        return