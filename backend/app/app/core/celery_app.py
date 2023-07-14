from celery import Celery
# from celery_sqlalchemy_scheduler.session import SessionManager

# celery app cconfiguration
celery_app = Celery('worker')
# Configure the Redis broker and backend
celery_app.conf.broker_url = 'redis://queue:6379'
celery_app.conf.result_backend = 'redis://queue:6379'

celery_app.conf.timezone = "Europe/Rome"

celery_app.conf.task_routes = {"app.worker.*": "main-queue"}



# beat_dburi = 'sqlite:///schedule.db'
# celery_app.conf.beat_dburi = beat_dburi

# database celery scheduler configuration
# session_manager = SessionManager()
# # engine, Session = session_manager.create_session(beat_dburi)
# # session = Session()

# def get_scheduler_db():
#     engine, Session = session_manager.create_session(beat_dburi)
#     return Session()

