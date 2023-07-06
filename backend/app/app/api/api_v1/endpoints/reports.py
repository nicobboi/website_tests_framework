from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from typing import List
from app.api import deps


router = APIRouter()

@router.post("/set", response_model=schemas.ReportCreate)
def create_report(
    *,
    db: Session = Depends(deps.get_db),
    report_in: schemas.ReportCreate,
) -> Any:
    """
    Create new report
    """
    report = crud.report.create(db, obj_in=report_in)

    return report
