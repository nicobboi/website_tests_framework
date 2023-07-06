from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from typing import List
from app.api import deps
from app import worker


router = APIRouter()

@router.get("/scores", response_model=List[schemas.ReportScores])
def get_reports_score(
    *,
    db: Session = Depends(deps.get_db),
    url: str
) -> Any: 
    """
    Get all reports scores by URL
    """
    reports_score = crud.report.get_scores(db=db, url=url)

    return reports_score


@router.post("/run", response_model=str)
def run_tests(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.WebsiteRun
) -> Any:
    worker.test_website.delay(uri=obj_in.url, test_type=obj_in.test_types)
    return "Run avviata!"