from app.core.celery_app import celery_app
from .tasks     import test_website
from .scheduler import add_schedule, rem_schedule, schedule_list