from raven import Client
import asyncio
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.celery_app import celery_app
from app.core.config import settings
from app.tools import use_tool

client_sentry = Client(settings.SENTRY_DSN)


# Celery tasks for test

# @celery_app.task
# def hello_world(word: str) -> str:
#     """
#     Test task
#     """
#     return f"test task return {word}"

# @celery_app.task
# def test_add(x, y):
#     return x + y


@celery_app.task
def test_website(url: str, test_type: str, scheduled: bool = True) -> str:
    """
    Start a test (by type) on the given url
    """
    use_tool.run_test(uri=url, test_type=test_type)
    # update schedule
    if scheduled:
        payload = {
            "min": None,
            "hour": None,
            "day": None,
            "active": None,
            "last_time_launched": str(datetime.now(tz=ZoneInfo("Europe/Rome"))),
        }
        params = {
            "schedule_url": url,
            "schedule_test_type": test_type
        }
        response = requests.post("http://backend/api/v1/schedule/update", params=params, json=payload)
    return "Tests ended."

