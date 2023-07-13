from celery import Celery
from celery_sqlalchemy_scheduler.session import SessionManager
from typing import Generator

# celery app cconfiguration
celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.timezone = "Europe/Rome"

celery_app.conf.task_routes = {"app.worker.*": "main-queue"}

beat_dburi = 'sqlite:///schedule.db'
celery_app.conf.beat_dburi = beat_dburi

# database celery scheduler configuration
session_manager = SessionManager()
# engine, Session = session_manager.create_session(beat_dburi)
# session = Session()

def get_scheduler_db():
    engine, Session = session_manager.create_session(beat_dburi)
    return Session()

