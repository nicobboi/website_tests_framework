from sqlalchemy.orm import Session
from sqlalchemy import asc

from pydantic import UUID4
from typing import Union

from app.crud.base import CRUDBase
from app import crud
from app.models import Report, Tool, Score, Website, Type
from app.schemas import ReportCreate, ReportUpdate, ReportTool, ReportScore, ReportDetails


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
        tool = db.query(Tool).filter(Tool.name == tool_name).first()
        if not tool:
            type_name = obj_in.tool.type
            type = db.query(Type).filter(Type.name == type_name).first()
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
                url=obj_in.url
            )
            db.add(website)
        website.reports.append(db_obj)

        db.commit()
        db.refresh(db_obj)

        # return a refactored schema output
        return ReportCreate(
            url=db_obj.website.url,
            tool=ReportTool(
                name=db_obj.tool.name,
                type=db_obj.tool.type.name
            ),
            scores=[ReportScore(
                name=score.name,
                score=score.score
            ) for score in db_obj.scores],
            notes=db_obj.notes,
            json_report=db_obj.json_report,
            start_test_timestamp=db_obj.start_test_timestamp,
            end_test_timestamp=db_obj.end_test_timestamp
        )
    

    def get(self, *, db: Session, id: UUID4) -> ReportDetails:
        """
        Get a report with formatted output by its id
        """
        report = crud.report.get_by_id(db=db, id=id)

        return ReportDetails(
            url=report.website.url,
            tool=ReportTool(name=report.tool.name, type=report.tool.type.name),
            scores=[ReportScore(name=score.name, score=score.score) for score in report.scores],
            notes=report.notes,
            end_test_time=report.end_test_timestamp,
            test_duration_time=test_time(start=report.start_test_timestamp, end=report.end_test_timestamp),
            json_report=report.json_report,
        )

    def get_all_filtered(self, *, db: Session, url: str, type: Union[str, None] = None):
        """
        Get all reports filtered by url (optional: filter by test type)
        """
        reports = crud.report.get_all_by_website(db=db, url=url, type_name=type, timestamp_order=True)

        return [ReportDetails(
            url=report.website.url,
            tool=ReportTool(name=report.tool.name, type=report.tool.type.name),
            scores=[ReportScore(name=score.name, score=score.score) for score in report.scores],
            notes=report.notes,
            end_test_time=report.end_test_timestamp,
            test_duration_time=test_time(start=report.start_test_timestamp, end=report.end_test_timestamp),
            json_report=report.json_report,
        ) for report in reports]

    def get_by_id(self, *, db: Session, id: UUID4) -> Report:
        """
        Get the report by its ID
        """
        return db.query(Report).filter(Report.id == id).first()
    
    def get_all_by_website(self, *, db: Session, url: str, type_name: Union[str, None] = None, timestamp_order: bool = False):
        """
        Get all the reports by the website associated (optional: timestamp order, tool type filter)
        """
        website = crud.website.get_by_url(db=db, url=url)
        if not website:
            return []
        
        main_query = db.query(Report).filter(Report.site_id == website.id)

        if type_name:
            type = db.query(Type).filter(Type.name == type_name).first()
            if type:
                main_query = main_query.join(Report.tool).filter(Tool.type_id == type.id)

        if timestamp_order:
            main_query = main_query.order_by(asc(Report.end_test_timestamp))

        return main_query.all()
    

def test_time(start, end):
    """
    Return the test time (string) between two datetime
    """

    test_duration = end - start

    if test_duration.seconds > 60:
        minutes = test_duration.seconds / 60
        seconds = int(60 * (minutes - int(minutes)))
        test_duration_str = "~" + str(int(minutes)) + ":" + str(seconds) + " min."
    else:
        test_duration_str = str(test_duration.seconds) + " s."

    return test_duration_str
    
report = CRUDReport(Report)
