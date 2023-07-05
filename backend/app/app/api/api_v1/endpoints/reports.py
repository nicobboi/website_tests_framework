from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


router = APIRouter()

@router.post("/", response_model=schemas.Report)
def create_report(
    *,
    db: Session = Depends(deps.get_db),
    report_in: schemas.ReportCreate,
) -> Any:
    """
    Create new report
    """
    report = crud.report.create(db, obj_in=report_in)

    return schemas.Report(
        notes=report.notes,
        json_report=report.json_report,
        timestamp=report.timestamp,
        tool=report.tool,
        scores=report.scores,
        website=report.website
    )

    #return report