from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings


router = APIRouter()

@router.post("/", response_model=schemas.ReportCreate)
def create_report(
    *,
    db: Session = Depends(deps.get_db),
    report_in: schemas.ReportCreate,
) -> Any:
    """
    Create new report
    """
    report = crud.report.create(db, obj_in=report_in)

    url = report_in.url
    website = crud.website.get_by_url(db, url=url)
    if not website:
        crud.website.create(db, obj_in=schemas.Website(url=url, reports=[report]))
    else:
        crud.website.append_new_report(db, website=website, report=report)

    return report