# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class  import Base  # noqa
from app.models.user    import User  # noqa
from app.models.token   import Token  # noqa
from app.models.report  import Report
from app.models.website import Website
from app.models.tool    import Tool
from app.models.score   import Score 