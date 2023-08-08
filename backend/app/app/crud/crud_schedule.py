from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app import crud
from app.models import Schedule, Website, Type
from app.schemas.schedule import ScheduleBase, ScheduleCreate


class CRUDSchedule(CRUDBase[Schedule, ScheduleBase, ScheduleBase]):
    # insert a new schdule into the db
    def create(self, db: Session, *, obj_in: ScheduleCreate):
        # schdule
        schedule = Schedule(
            active=True,
            schedule=obj_in.info
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
            type.schdules.append(schedule)

        db.commit()

        return
    
    # get a schdule instance by its ID
    def get_by_id(self, db: Session, *, id) -> Schedule:
        return db.query(Schedule).filter(Schedule.id == id).first()
    
    # change status of a schedule task
    def change_status(self, db: Session, *, id) -> bool:
        schedule = self.get_by_id(db=db, id=id)

        schedule.active = not schedule.active
        
        db.commit()
    
    def get_all_active(self, db: Session) -> list[dict]:
        """
        Get all schedules
        """
        schedules = db.query(Schedule).filter(Schedule.active == True).all()

        return [{
            "url": schedule.website.url,
            "test_type": schedule.type.name,
            "info": schedule.schedule,
            "last_time_launched": schedule.last_time_launched
        } for schedule in schedules]

schedule = CRUDSchedule(Schedule)