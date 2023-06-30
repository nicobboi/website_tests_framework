from datetime import datetime

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportUpdate


class CRUDReport(CRUDBase[Report, ReportCreate, ReportUpdate]):
    def create(self, db: Session, *, obj_in: ReportCreate):
        db_obj = Report(
            notes=obj_in.notes,
            json_report=obj_in.json_report,
            timestamp=datetime.now(),
            tool=obj_in.tool,
            scores=obj_in.scores
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
    
report = CRUDReport(Report)