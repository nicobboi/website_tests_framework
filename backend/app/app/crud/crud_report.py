from datetime import datetime

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app import crud
from app.models.report import Report
from app.models.tool import Tool
from app.models.score import Score
from app.models.website import Website
from app.schemas.report import ReportCreate, ReportUpdate


class CRUDReport(CRUDBase[Report, ReportCreate, ReportUpdate]):
    def create(self, db: Session, *, obj_in: ReportCreate):
        db_obj = Report(
            notes=obj_in.notes,
            json_report=obj_in.json_report,
            timestamp=datetime.now(),
        )
        db.add(db_obj)

        # Score relationship
        for s in obj_in.scores:
            score = Score(
                name=s.name,
                score=s.score
            )
            db.add(score)
            db_obj.scores.append(score)

        # Tool relationship
        tool_name = obj_in.tool.name
        tool = crud.tool.get_by_name(db=db, name=tool_name)
        if not tool:
            tool = Tool(
                name=tool_name,
                type=obj_in.tool.type
            )
            db.add(tool)
        db_obj.tool = tool

        # Website relationship
        url = obj_in.url
        website = crud.website.get_by_url(db, url=url)
        if not website:
            website = Website(
                url=obj_in.url,
                reports=[db_obj]
            )
            db.add(website)
        else:
            website.reports.append(db_obj)
        db_obj.website = website

        db.commit()
        db.refresh(db_obj)

        return db_obj
    
report = CRUDReport(Report)