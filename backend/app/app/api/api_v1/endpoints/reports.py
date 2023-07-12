from typing import Any
from datetime import datetime

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
            "start_test_timestamp": datetime.now(),
            "end_test_timestamp": datetime.now(),
            "tool": {
                "name": "tool_name",
                "type": "tool_type"
            },
            "scores": [
                {
                "name": "overall",
                "score": 100
                }
            ],
            "url": "http://websiteurl"
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
