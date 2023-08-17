from typing import Any, Union
from pydantic import UUID4
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps


router = APIRouter()


@router.get("/get", response_model=schemas.ReportDetails)
def get_report(
    id: UUID4,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a report by its id
    """
    return crud.report.get(db=db, id=id)

@router.get("/get-all-filtered", response_model=list[schemas.ReportDetails])
def get_reports(
    url: str, 
    type: Union[str, None] = None,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get all reports by url (optional: filter by type)
    """
    return crud.report.get_all_filtered(db=db, url=url, type=type)


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
    return crud.report.create(db, obj_in=report_in)
