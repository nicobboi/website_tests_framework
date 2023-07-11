from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app import crud
from app.models import Crontab, Website, Type
from app.schemas.crontab import CrontabBase, CrontabCreate


class CRUDCrontab(CRUDBase[Crontab, CrontabBase, CrontabBase]):
    # insert a new crontab into the db
    def create(self, db: Session, *, obj_in: CrontabCreate) -> Crontab:
        # crontab
        crontab = Crontab(
            active=True,
            crontab=obj_in.info
        )
        db.add(crontab)

        # website
        url = obj_in.url
        website = crud.website.get_by_url(db=db, url=url)
        if not website:
            website = Website(
                url=url
            )
            db.add(website)
        website.crontabs.append(crontab)

        # verifica tipi
        for type_name in obj_in.test_types:
            type = crud.type.get_by_name(db=db, name=type_name)
            if not type:
                type = Type(
                    name=type_name
                )
                db.add(type)
            type.crontabs.append(crontab)

        db.commit()

        return Crontab
    
    # get a crontab instance by its ID
    def get_by_id(self, db: Session, *, id) -> Crontab:
        return db.query(Crontab).filter(Crontab.id == id).first()
    
    # change status of a crontab task
    def change_status(self, db: Session, *, id) -> bool:
        crontab = self.get_by_id(db=db, id=id)

        crontab.active = not crontab.active
        
        db.commit()
    
crontab = CRUDCrontab(Crontab)