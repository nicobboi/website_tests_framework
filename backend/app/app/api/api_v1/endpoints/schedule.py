from typing import Any
from datetime import datetime
from pydantic import UUID4
from typing import Union

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

from app.worker import scheduler


router = APIRouter()

@router.get("/get-all", response_model=list[schemas.ScheduleOutput])
def get_all_schedules(*, db: Session = Depends(deps.get_db)):
    """
    Get all schedules
    """

    return crud.schedule.get_all(db=db)

@router.get("/get", response_model=Union[schemas.ScheduleOutput, None])
def get_schedule(
    *, 
    db: Session = Depends(deps.get_db),
    scheduler_id: Union[UUID4, None] = None,
    scheduler_url: Union[str, None] = None,
    scheduler_test_type: Union[str, None] = None
) -> Any:
    """
    Get a schedule by ID, url or/and type
    """
    if scheduler_id:
        schedule = crud.schedule.get_by_id(db=db, id=scheduler_id)
    elif scheduler_url and scheduler_test_type:
        schedule = crud.schedule.get_by_url(db=db, url=scheduler_url, type_name=scheduler_test_type)

    print(str(schedule))

    if schedule:
        return schemas.ScheduleOutput(
            id=schedule.id,
            url=scheduler_url,
            test_type=scheduler_test_type,
            schedule_info=schemas.ScheduleBase(
                min=schedule.min,
                hour=schedule.hour,
                day=schedule.day
            ),
            active=schedule.active,
            n_run=schedule.n_run,
            scheduled_time=schedule.scheduled_time,
            last_time_launched=schedule.last_time_launched
        )
    else: return None


@router.post("/add", response_model=list[schemas.ScheduleOutput])
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
    added_schedules = crud.schedule.create(db=db, obj_in=schedule_in)

    # start schedule with scheduler
    for schedule in added_schedules:
        scheduler.add_schedule(
            url=schedule.url,
            schedule_name=str(schedule.id),
            test_type=schedule.test_type,
            schedule_time=scheduler.ScheduleInfo(
                min=schedule.schedule_info.min,
                hour=schedule.schedule_info.hour,
                day=schedule.schedule_info.day
            )
        )

    return added_schedules 


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

    scheduler.rem_schedule(schedule_name=str(removed_schedule.id))

    return removed_schedule


@router.post("/update", response_model=Union[schemas.ScheduleOutput, None])
def update_schedule(
    *,
    db: Session = Depends(deps.get_db),
    schedule_id: Union[UUID4, None] = None,
    schedule_url: Union[str, None] = None,
    schedule_test_type: Union[str, None] = None,
    schedule_in: schemas.ScheduleUpdate = Body(
        example={
            "min": 1,
            "hour": 5,
            "day": 1,
            "active": True,
            "last_time_launched": datetime.now()
        }
    )
) -> Any:
    """
    Update a schedule and return it
    """
    try:
        updated_schedule, was_active = crud.schedule.update(
            db=db, 
            id=schedule_id, 
            url=schedule_url,
            test_type=schedule_test_type,
            obj_in=schedule_in
        )
    except AttributeError:
        return None

    # update schedule from the scheduler (remove and re-add)
    # if was active and now is disabled, remove from scheduler
    if was_active and not updated_schedule.active:
        scheduler.rem_schedule(str(updated_schedule.id))
    # if wasn't active and now is enabled, add to the scheduler
    elif not was_active and updated_schedule.active:
        scheduler.add_schedule(
            url=updated_schedule.url,
            schedule_name=str(updated_schedule.id),
            test_type=updated_schedule.test_type,
            schedule_time=scheduler.ScheduleInfo(
                min=updated_schedule.schedule_info.min,
                hour=updated_schedule.schedule_info.hour,
                day=updated_schedule.schedule_info.day
            )
        )
    # if is still active, remove and readd to update schedule
    elif was_active and updated_schedule.active:
        scheduler.rem_schedule(str(updated_schedule.id))
        scheduler.add_schedule(
            url=updated_schedule.url,
            schedule_name=str(updated_schedule.id),
            test_type=updated_schedule.test_type,
            schedule_time=scheduler.ScheduleInfo(
                min=updated_schedule.schedule_info.min,
                hour=updated_schedule.schedule_info.hour,
                day=updated_schedule.schedule_info.day
            )
        )

    return updated_schedule