from sqlalchemy.orm import Session
from sqlalchemy import asc

from typing import Union
from pydantic import UUID4

from app.crud.base import CRUDBase
from app import crud
from app.models import Schedule, Website, Type, ScheduleInfo
from app.schemas.schedule import ScheduleBase, ScheduleCreate, ScheduleUpdate, ScheduleOutput

from datetime import datetime, timezone




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
                scheduled_time=datetime.now(tz=timezone.utc)
            )
            db.add(schedule)

            # schedule info
            schedule_info = db.query(ScheduleInfo).filter(
                ScheduleInfo.time        == obj_in.time_info and \
                set(ScheduleInfo.days)   == set(obj_in.days)
            ).first()
            if not schedule_info:  
                schedule_info = ScheduleInfo(
                    time=obj_in.time_info,
                    days=obj_in.days
                )
                db.add(schedule_info)

            schedule_info.schedules.append(schedule)
                

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
            type = db.query(Type).filter(Type.name == test_type).first()
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
                    time_info=schedule_info.time,
                    days=schedule_info.days
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
                time_info=schedule.schedule_info.time,
                days=schedule.schedule_info.days
            ),
            active=schedule.active,
            n_run=schedule.n_run,
            scheduled_time=schedule.scheduled_time,
            last_time_launched=schedule.last_time_launched
        )

        db.delete(schedule)

        db.commit()

        return output

    def update(
        self, 
        db: Session, 
        *, 
        id: Union[UUID4, None] = None, 
        url: Union[str, None] = None , 
        test_type: Union[str, None] = None, 
        obj_in: ScheduleUpdate
    ) -> Union[ScheduleOutput, bool, None]:
        """
        Update a schedule (return updated schedule and if it was active before update)
        """
        schedule = None
        if id:                  schedule = self.get_by_id(db=db, id=id)
        elif url and test_type: schedule = self.get_by_url(db=db, url=url, type_name=test_type)
        if not schedule:        raise AttributeError

        was_active = schedule.active

        if obj_in.time_info:        schedule.schedule_info.time = obj_in.time_info
        if obj_in.days:             schedule.schedule_info.days = obj_in.days
        if obj_in.active != None:   schedule.active = obj_in.active
        if obj_in.last_time_launched and (schedule.last_time_launched != obj_in.last_time_launched):
            schedule.last_time_launched = obj_in.last_time_launched
            schedule.n_run = schedule.n_run + 1
        
        db.commit()

        return ScheduleOutput(
            id=schedule.id,
            url=schedule.website.url,
            test_type=schedule.type.name,
            schedule_info=ScheduleBase(
                time_info=schedule.schedule_info.time,
                days=schedule.schedule_info.days
            ),
            active=schedule.active,
            n_run=schedule.n_run,
            scheduled_time=schedule.scheduled_time,
            last_time_launched=schedule.last_time_launched
        ), was_active


    def get(
        self, 
        db: Session, 
        *, 
        scheduler_id: Union[UUID4, None] = None,
        scheduler_url: Union[str, None] = None,
        scheduler_test_type: Union[str, None] = None
    ) -> Union[ScheduleOutput, None]:
        """
        Get a schedule by its id or url and test_type
        """

        if scheduler_id:
            schedule = crud.schedule.get_by_id(db=db, id=scheduler_id)
        elif scheduler_url and scheduler_test_type:
            schedule = crud.schedule.get_by_url(db=db, url=scheduler_url, type_name=scheduler_test_type)

        if schedule:
            return ScheduleOutput(
                id=schedule.id,
                url=scheduler_url,
                test_type=scheduler_test_type,
                schedule_info=ScheduleBase(
                    time_info=schedule.schedule_info.time,
                    day=schedule.schedule_info.days
                ),
                active=schedule.active,
                n_run=schedule.n_run,
                scheduled_time=schedule.scheduled_time,
                last_time_launched=schedule.last_time_launched
            )
        else: return None

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

    def get_all(self, db: Session, *, active: bool = False) -> list[ScheduleOutput]:
        """
        Get all schedules
        """
        main_query = db.query(Schedule).join(Schedule.website).order_by(asc(Website.url))
        if active: main_query = main_query.filter(Schedule.active == True)

        schedules = main_query.all()

        return [ScheduleOutput(
            id=schedule.id,
            url=schedule.website.url,
            test_type=schedule.type.name,
            schedule_info=ScheduleBase(
                time_info=schedule.schedule_info.time,
                days=schedule.schedule_info.days
            ),
            active=schedule.active,
            scheduled_time=schedule.scheduled_time,
            n_run=schedule.n_run,
            last_time_launched=schedule.last_time_launched
        ) for schedule in schedules]


schedule = CRUDSchedule(Schedule)