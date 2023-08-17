# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class  import Base  # noqa
from app.models.report  import Report
from app.models.website import Website
from app.models.tool    import Tool
from app.models.score   import Score 
from app.models.type    import Type
from app.models.schedule import Schedule
from app.models.scheduleinfo import ScheduleInfo