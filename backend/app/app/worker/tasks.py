from raven import Client
import asyncio

from app.core.celery_app import celery_app
from app.core.config import settings
from app.tools import use_tool

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task
def hello_world(word: str) -> str:
    """
    Test task
    """
    return f"test task return {word}"


@celery_app.task
def test_website(uri: str, test_type: str) -> str:
    """
    Start a test (by type) on the given url
    """
    use_tool.run_test(uri=uri, test_type=test_type)
    return "Tests ended."

