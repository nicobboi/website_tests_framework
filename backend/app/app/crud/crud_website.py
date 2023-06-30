from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Website, Report
from app.schemas.website import WebsiteCreate, WebsiteUpdate


class CRUDWebsite(CRUDBase[Website, WebsiteCreate, WebsiteUpdate]):
    # create new website item
    def create(self, db: Session, *, obj_in: WebsiteCreate) -> Website:
        db_obj = Website(
            url=obj_in.url,
            reports=obj_in.reports
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
    
    # append a new report into the website
    def append_new_report(self, db: Session, *, website: Website, report: Report):
        website.reports.append(report)
        db.merge(website)
        db.commit()
    
    # return a website item by its url
    def get_by_url(self, db: Session, *, url: str) -> Website:
        return db.query(Website).filter(Website.url == url).first()
    
website = CRUDWebsite(Website)