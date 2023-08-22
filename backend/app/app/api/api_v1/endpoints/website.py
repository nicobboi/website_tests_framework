from typing import Any, List, Optional, Union
from pydantic import UUID4

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app import crud, schemas, worker
from app.api import deps
from celery import group

router = APIRouter()


@router.get("/scores", response_model=Union[schemas.WebsiteReportsScores, List])
def get_website_scores(
    *, 
    db: Session = Depends(deps.get_db), 
    website_url: Optional[str] = None, 
    website_id: Optional[UUID4] = None
) -> Any:
    """
    Get all website's scores by URL or ID
    """
    if not website_url and not website_id:
        return []

    website_scores = crud.website.get_scores(db=db, url=website_url, id=website_id)

    return website_scores


@router.get("/latest-scores", response_model=Union[List[schemas.AllWebsiteScores], List])
def get_all_website_latest_scores(
    *,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get latest scores of all websites
    """
    return crud.website.get_all_latest_scores(db=db)


@router.get("/average-scores", response_model=Union[List[schemas.AllWebsiteScores], List])
def get_all_website_average_scores(
    *,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get average scores of all websites
    """
    return crud.website.get_all_average_scores(db=db)


@router.post("/run")
def run_tests(
    *,
    obj_in: schemas.WebsiteRun = Body(
        example={
            "url": "https://www.comune.novellara.re.it/",
            "test_types": ["accessibility", "performance", "security", "seo", "validation"],
        }
    ),
    repeat_test: Union[int, None] = 1,
) -> Any:
    """
    Launch a different Celery task for all the test types given to test the website. <br />
    <strong>Test types</strong>:
        <br/>"accessibility",
        <br/>"performance",
        <br/>"security",
        <br/>"seo",
        <br/>"validation",
    """
    for time in range(1, repeat_test+1):
        try:
            job = group(worker.test_website.s(url=obj_in.url, test_type=test, scheduled=False) for test in obj_in.test_types)
            res = job.apply_async()
        except worker.test_website.OperationalError as e:
            print("Sending task raised: " + str(e) + "\n")
    return [{
        "task_id": res[0][0],
        "url": obj_in.url
        } for res in res.as_tuple()[1]] # return all tasks id

