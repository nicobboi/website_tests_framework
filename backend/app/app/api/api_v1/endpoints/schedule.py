from typing import Any
from datetime import datetime
from pydantic import UUID4

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


router = APIRouter()

@router.get("/get-all", response_model=list[schemas.ScheduleOutput])
def get_all_schedules(*, db: Session = Depends(deps.get_db)):
    """
    Get all schedules
    """

    return crud.schedule.get_all(db=db)


@router.post("/add")
def add_schedule(
    *, 
    db: Session = Depends(deps.get_db), 
    schedule_in: schemas.ScheduleCreate = Body(
        example={
            "min": 5,
            "hour": 12,
            "day": 1,
            "url": "https://www.comune.novellara.re.it/",
            "test_types": [
                "accessibility",
                "performance"
            ]
        }
    ),
) -> Any:
    """
    Add a new schedule to db
    """
    schedule_model = crud.schedule.create(db=db, obj_in=schedule_in)

    # start schedule with scheduler


@router.post("/remove", response_model=schemas.ScheduleOutput)
def rem_schedule(
    *, 
    db: Session = Depends(deps.get_db), 
    schedule_id: UUID4,
) -> Any:
    """
    Remove a schedule from the db and return it
    """
    removed_schedule = crud.schedule.remove(db=db, id=schedule_id)

    # remove schedule from scheduler

    return removed_schedule


@router.post("/update", response_model=schemas.ScheduleOutput)
def update_scheduler(
    *,
    db: Session = Depends(deps.get_db),
    scheduler_id: UUID4,
    schedule_in: schemas.ScheduleUpdate = Body(
        example={
            "min": 1,
            "hour": 5,
            "day": 1,
            "active": True
        }
    )
) -> Any:
    """
    Update a schedule and return it
    """
    updated_schedule = crud.schedule.update(db=db, id=scheduler_id, obj_in=schedule_in)
    
    # update schedule from the scheduler (remove and re-add)

    return update_scheduler