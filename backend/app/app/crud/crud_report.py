from datetime import datetime
from pydantic import UUID4

from sqlalchemy.orm import Session
from sqlalchemy import asc

from app.crud.base import CRUDBase
from app import crud
from app.models import Report, Tool, Score, Website, Type
from app.schemas.report import ReportCreate, ReportUpdate, ReportScores
from app.schemas import ReportScores, ToolBase, ScoreBase


class CRUDReport(CRUDBase[Report, ReportCreate, ReportUpdate]):
    def create(self, db: Session, *, obj_in: ReportCreate):
        """
        insert a new report into the db
        """
        db_obj = Report(
            notes=obj_in.notes,
            json_report=obj_in.json_report,
            start_test_timestamp=obj_in.start_test_timestamp,
            end_test_timestamp=obj_in.end_test_timestamp
        )
        db.add(db_obj)

        # Score relationship
        if obj_in.scores:
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
            type_name = obj_in.tool.type
            type = crud.type.get_by_name(db=db, name=type_name)
            if not type:
                type = Type(name=type_name)
            db.add(type)

            tool = Tool(
                name=tool_name,
                type=type
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

        # return a refactored schema output
        return ReportCreate(
            url=db_obj.website.url,
            tool=ToolBase(
                name=db_obj.tool.name,
                type=db_obj.tool.type.name
            ),
            scores=[ScoreBase(
                name=score.name,
                score=score.score
            ) for score in db_obj.scores],
            notes=db_obj.notes,
            json_report=db_obj.json_report,
            start_test_timestamp=db_obj.start_test_timestamp,
            end_test_timestamp=db_obj.end_test_timestamp
        )
    
    def get_by_id(self, *, db: Session, id: UUID4) -> Report:
        """
        Get the report by its ID
        """
        return db.query(Report).filter(Report.id == id).first()
    
    def get_by_website(self, *, db: Session, url: str, timestamp_order: bool = False):
        """
        Get all the reports by the website associated (optional: timestamp order)
        """
        website = crud.website.get_by_url(db=db, url=url)
        if not website:
            return []

        if timestamp_order:
            return db.query(Report).filter(Report.site_id == website.id).order_by(asc(Report.end_test_timestamp)).all()
        else:
            return db.query(Report).filter(Report.site_id == website.id).all()
    

    
report = CRUDReport(Report)
