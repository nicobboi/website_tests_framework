from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app import crud
from app.models import Schedule, Website, Type
from app.schemas.schedule import ScheduleBase, ScheduleCreate, ScheduleUpdate, ScheduleOutput

from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import UUID4
from typing import Union


class CRUDSchedule(CRUDBase[Schedule, ScheduleCreate, ScheduleUpdate]):

    def create(self, db: Session, *, obj_in: ScheduleCreate) -> list[ScheduleOutput]:
        """
        insert a new schedule into the db
        """
        schedule_added = []

        for test_type in obj_in.test_types:
            # check if already exist a schedule for this url and test_type
            if self.get_by_url(db=db, url=obj_in.url, type_name=test_type):
                break

            # schedule
            schedule = Schedule(
                active=True,
                min=obj_in.min,
                hour=obj_in.hour,
                day=obj_in.day,
                scheduled_time=str(datetime.now())
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
            type = crud.type.get_by_name(db=db, name=test_type)
            if not type:
                type = Type(
                    name=test_type
                )
                db.add(type)
            type.schedules.append(schedule)

            db.commit()

            schedule_added.append(ScheduleOutput(
                id=schedule.id,
                url=website.url,
                test_type=type.name,
                schedule_info=ScheduleBase(
                    min=schedule.min,
                    hour=schedule.hour,
                    day=schedule.day
                ),
                active=schedule.active,
                n_run=schedule.n_run,
                scheduled_time=schedule.scheduled_time,
                last_time_launched=schedule.last_time_launched
            ))

        return schedule_added
    
    def remove(self, db: Session, *, id: UUID4) -> ScheduleOutput:
        """
        Remove a schedule by its id and return it
        """
        schedule = self.get_by_id(db=db, id=id)

        output = ScheduleOutput(
            id=schedule.id,
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

        db.delete(schedule)

        db.commit()

        return output

    def update(self, db: Session, *, id: UUID4, obj_in: ScheduleUpdate) -> ScheduleOutput:
        """
        Update a schedule
        """
        schedule = self.get_by_id(db=db, id=id)

        schedule.min = obj_in.min
        schedule.hour = obj_in.hour
        schedule.day = obj_in.day
        schedule.active = obj_in.active
        
        db.commit()

        return ScheduleOutput(
            id=schedule.id,
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


    def get_by_id(self, db: Session, *, id: UUID4) -> Schedule:
        """
        Get a schedule instance by its ID
        """
        return db.query(Schedule).filter(Schedule.id == id).first()
    
    def get_by_url(self, db: Session, *, url: str, type_name: Union[str, None] = None) -> Schedule:
        """
        Get a schedule instance from the db by its url (optional: filter by type_name)
        """
        main_query = db.query(Schedule).join(Schedule.website).filter(Website.url == url)

        if type_name:
            main_query = main_query.join(Schedule.type).filter(Type.name == type_name)

        return main_query.first()

    def get_all(self, db: Session) -> list[ScheduleOutput]:
        """
        Get all schedules
        """
        schedules = db.query(Schedule).all()

        return [ScheduleOutput(
            id=schedule.id,
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