from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from celery import group
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
    obj_in: schemas.WebsiteRun
) -> Any:
    try:
        job = group(worker.test_website.s(uri=obj_in.url, test_type=test) for test in obj_in.test_types)

        job.apply_async()
    except worker.test_website.OperationalError as e:
        print("Sending task raised: " + str(e) + "\n")
    return "Run avviata!"