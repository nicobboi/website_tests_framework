from app.core.celery_app import celery_app
from .tasks     import test_website, hello_world
from .scheduler import add_schedule, remove_schedule