from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app import crud
from app.models import Schedule, Website, Type
from app.schemas.schedule import ScheduleBase, ScheduleCreate, ScheduleUpdate, ScheduleOutput

from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import UUID4


class CRUDSchedule(CRUDBase[Schedule, ScheduleCreate, ScheduleUpdate]):
    # insert a new schedule into the db
    def create(self, db: Session, *, obj_in: ScheduleCreate):
        # schedule
        schedule = Schedule(
            active=True,
            min=obj_in.min,
            hour=obj_in.hour,
            day=obj_in.day,
            scheduled_time=datetime.now()
        )
        db.add(schedule)

        # website
        url = obj_in.url
        website = crud.website.get_by_url(db=db, url=url)
        if not website:
            website = Website(
                url=url
            )
            db.add(website)
        website.schedules.append(schedule)

        # verifica tipi
        for type_name in obj_in.test_types:
            type = crud.type.get_by_name(db=db, name=type_name)
            if not type:
                type = Type(
                    name=type_name
                )
                db.add(type)
            type.schedules.append(schedule)

        db.commit()

        return
    
    def remove(self, db: Session, *, id: UUID4) -> ScheduleOutput:
        """
        Remove a schedule by its id and return it
        """
        schedule = self.get_by_id(db=db, id=id)

        db.delete(schedule)

        db.commit()

        return ScheduleOutput(
            url=schedule.website.url,
            test_type=schedule.type.name,
            schedule_info=ScheduleBase(
                min=schedule.min,
                hour=schedule.hour,
                day=schedule.day
            ),
            active=schedule.active,
            n_run=schedule.n_run,
            scheduled_time=schedule.scheduled_time,
            last_time_launched=schedule.last_time_launched
        )

    # change status of a schedule task
    def update(self, db: Session, *, id: UUID4, obj_in: ScheduleUpdate) -> ScheduleOutput:
        schedule = self.get_by_id(db=db, id=id)

        schedule.active = not schedule.active
        
        db.commit()

        return schedule.active


    def get_by_id(self, db: Session, *, id: UUID4) -> Schedule:
        """
        Get a schedule instance by its ID
        """
        return db.query(Schedule).filter(Schedule.id == id).first()
    

    def get_all(self, db: Session) -> list[dict]:
        """
        Get all schedules
        """
        schedules = db.query(Schedule).all()

        return [ScheduleOutput(
            url=schedule.website.url,
            test_type=schedule.type.name,
            schedule_info=ScheduleBase(
                min=schedule.min,
                hour=schedule.hour,
                day=schedule.day
            ),
            active=schedule.active,
            scheduled_time=schedule.scheduled_time,
            n_run=schedule.n_run,
            last_time_launched=schedule.last_time_launched
        ) for schedule in schedules]

schedule = CRUDSchedule(Schedule)