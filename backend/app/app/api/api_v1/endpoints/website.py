from typing import Any

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import Union

from app import crud, models, schemas
from celery import group
from typing import List, Optional
from pydantic import UUID4
from app.api import deps
from app import worker


router = APIRouter()

@router.get("/scores", response_model=Union[schemas.WebsiteReportsScores,List])
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

@router.post("/run", response_model=str)
def run_tests(
    *,
    obj_in: schemas.WebsiteRun = Body(
        example={
            "url": "https://www.comune.novellara.re.it/",
            "test_types": [
                "performance",
                "security"
            ]
        }
    )
) -> Any:
    """
    Launch a different Celery task for all the test types given to test the website. <br />
    <strong>Test types<strong />:
        <br/>accessibility,
        <br/>performance,
        <br/>security,
        <br/>seo,
        <br/>validation.
    """
    try:
        job = group(worker.test_website.s(uri=obj_in.url, test_type=test) for test in obj_in.test_types)

        job.apply_async()
    except worker.test_website.OperationalError as e:
        print("Sending task raised: " + str(e) + "\n")
    return "Run avviata!"


@router.post("/schedule", response_model=str)
def set_schedule(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.WebsiteSchedule
) -> Any:
    crontab_model = crud.crontab.create(db=db, obj_in=schemas.CrontabCreate(
        info=obj_in.crontab,
        url=obj_in.url,
        test_types=obj_in.test_types
    ))

    worker.schedule_tasks()

    # TODO start new scheduled tasks with crontab info
    # try:
    #     scheduler.setup_periodic_tasks(crontab_conf=obj_in.crontab, url=obj_in.url, test_types=obj_in.test_types, id=crontab_model.id)
    #     return "Scheduler started!"
    # except Exception as e:
    #     return "An exception occurred: " + str(e)

    return "Fatto"




@router.post("/scheduler/setstatus")
def change_scheduler_status(
    *,
    db: Session = Depends(deps.get_db),
    scheduler_name, # id crontab in the db
) -> Any:
    # TODO: attivare/disattivare scheduler

    # change the status of a crontab task
    crud.crontab.change_status(db=db, id=scheduler_name)

    return "Scheduler status modified!"