from typing import Any, Union
from datetime import datetime, timezone, timedelta
from pydantic import UUID4

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


router = APIRouter()


@router.post("/set", response_model=schemas.ReportCreate)
def create_report(
    report_in: schemas.ReportCreate = Body(
        example={
            "notes": "Some notes...",
            "json_report": {},
            "start_test_timestamp": datetime.now(timezone.utc),
            "end_test_timestamp": datetime.now(timezone.utc) + timedelta(minutes=10),
            "tool": {"name": "tool_name", "type": "tool_type"},
            "scores": [{"name": "overall", "score": 100}],
            "url": "http://websiteurl",
        }
    ),
    *,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Insert a report into the database
    """
    report = crud.report.create(db, obj_in=report_in)

    return report


@router.get("/get", response_model=schemas.ReportDetails)
def get_report(
    id: UUID4,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a report by its id
    """

    report = crud.report.get_by_id(db=db, id=id)

    test_duration = report.end_test_timestamp - report.start_test_timestamp

    if test_duration.seconds > 60:
        minutes = test_duration.seconds / 60
        seconds = int(60 * (minutes - int(minutes)))
        test_duration_str = "~" + str(int(minutes)) + ":" + str(seconds) + " min."
    else:
        test_duration_str = str(test_duration.seconds) + " s."

    return schemas.ReportDetails(
        url=report.website.url,
        tool=schemas.ToolBase(name=report.tool.name, type=report.tool.type.name),
        scores=[schemas.ScoreBase(name=score.name, score=score.score) for score in report.scores],
        notes=report.notes,
        end_test_time=report.end_test_timestamp,
        test_duration_time=test_duration_str,
        json_report=report.json_report,
    )

@router.get("/get-all-filtered", response_model=list[schemas.ReportDetails])
def get_reports(
    url: str, 
    type: Union[str, None] = None,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get all reports by url (optional: filter by type)
    """
    reports = crud.report.get_all_by_website(db=db, url=url, type_name=type, timestamp_order=True)

    def test_time(start, end):
        test_duration = end - start

        if test_duration.seconds > 60:
            minutes = test_duration.seconds / 60
            seconds = int(60 * (minutes - int(minutes)))
            test_duration_str = "~" + str(int(minutes)) + ":" + str(seconds) + " min."
        else:
            test_duration_str = str(test_duration.seconds) + " s."

        return test_duration_str

    return [schemas.ReportDetails(
        url=report.website.url,
        tool=schemas.ToolBase(name=report.tool.name, type=report.tool.type.name),
        scores=[schemas.ScoreBase(name=score.name, score=score.score) for score in report.scores],
        notes=report.notes,
        end_test_time=report.end_test_timestamp,
        test_duration_time=test_time(report.start_test_timestamp, report.end_test_timestamp),
        json_report=report.json_report,
    ) for report in reports]
