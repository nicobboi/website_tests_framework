from raven import Client
import asyncio
from typing import List

from app.core.celery_app import celery_app
from app.core.config import settings
from app.tools import use_tool

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(acks_late=True)
async def test_celery(word: str) -> str:
    await asyncio.sleep(5)
    return f"test task return {word}"


@celery_app.task
def test_website(uri: str, test_type: List[str]) -> str:
    use_tool.run_tests(uri=uri, test_type=test_type)
    return "Tests ended."

