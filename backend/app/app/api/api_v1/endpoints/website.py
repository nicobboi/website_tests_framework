from typing import Any

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import Union

from app import crud, models, schemas
from celery import group
from typing import List
from app.api import deps
from app import worker
#from app import scheduler


router = APIRouter()

@router.get("/scores", response_model=Union[List[schemas.ReportScores],None])
def get_reports_score(
    *,
    db: Session = Depends(deps.get_db),
    url: str = Body(
        example={
            "url": "http://websiteurl"
        }
    )
) -> Any: 
    """
    Get all reports scores by URL
    """
    reports_score = crud.website.get_scores(db=db, url=url)

    return reports_score


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

    # TODO start new scheduled tasks with crontab info
    # try:
    #     scheduler.setup_periodic_tasks(crontab_conf=obj_in.crontab, url=obj_in.url, test_types=obj_in.test_types, id=crontab_model.id)
    #     return "Scheduler started!"
    # except Exception as e:
    #     return "An exception occurred: " + str(e)




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