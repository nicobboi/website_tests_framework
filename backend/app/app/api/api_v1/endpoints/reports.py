from typing import Any, Annotated
from datetime import datetime

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app import crud, models, schemas
from typing import List
from app.api import deps


router = APIRouter()

@router.post("/set", response_model=schemas.ReportCreate)
def create_report(
    report_in: Annotated[
        schemas.ReportCreate,
        Body(
            examples=[
                {
                    "notes": "Some notes...",
                    "json_report": {},
                    "start_test_timestamp": "2023-07-12T13:20:14.530",
                    "end_test_timestamp": "2023-07-12T13:20:14.530",
                    "tool": {
                        "name": "string",
                        "type": "string"
                    },
                    "scores": [
                        {
                        "name": "string",
                        "score": 0
                        }
                    ],
                    "url": "string"
                }
            ],
        ),
    ],
    *,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Insert a report into the database
    """
    report = crud.report.create(db, obj_in=report_in)

    return report
