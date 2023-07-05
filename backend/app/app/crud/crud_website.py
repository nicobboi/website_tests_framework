from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Website, Report
from app.schemas.website import WebsiteCreate, WebsiteUpdate


class CRUDWebsite(CRUDBase[Website, WebsiteCreate, WebsiteUpdate]):
    # return a website item by its url
    def get_by_url(self, db: Session, *, url: str) -> Website:
        return db.query(Website).filter(Website.url == url).first()
    
website = CRUDWebsite(Website)