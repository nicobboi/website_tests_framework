from typing import Any, Union
from pydantic import UUID4
from datetime import datetime, time, timezone

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app import crud, schemas
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
    return crud.schedule.get(
        db=db,
        scheduler_id=scheduler_id,
        scheduler_url=scheduler_url,
        scheduler_test_type=scheduler_test_type
    )


@router.post("/add", response_model=list[schemas.ScheduleOutput])
def add_schedule(
    *, 
    db: Session = Depends(deps.get_db), 
    schedule_in: schemas.ScheduleCreate = Body(
        example={
            "time_info": time(hour=13, minute=46, tzinfo=timezone.utc),
            "days": [
                "monday",
                "saturday"
            ],
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
                time_info=schedule.schedule_info.time_info,
                days=schedule.schedule_info.days
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
            "time_info": time(hour=13, minute=46, tzinfo=timezone.utc),
            "days": [
                "monday",
                "saturday"
            ],
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
                time_info=updated_schedule.schedule_info.time_info,
                days=updated_schedule.schedule_info.days
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
                time_info=updated_schedule.schedule_info.time_info,
                days=updated_schedule.schedule_info.days
            )
        )

    return updated_schedule