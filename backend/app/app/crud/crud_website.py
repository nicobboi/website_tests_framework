from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Website, Report
from app.schemas.website import WebsiteCreate, WebsiteUpdate
from app.schemas import ReportScores, ToolBase, ScoreBase

class CRUDWebsite(CRUDBase[Website, WebsiteCreate, WebsiteUpdate]):
    # return all reports scores from a given URL
    def get_scores(self, db: Session, *, url: str):
        website = self.get_by_url(db=db, url=url)
        if not website:
            return []

        # return a refactored schema output
        return [ReportScores(
            tool=ToolBase(
                name=report.tool.name,
                type=report.tool.type.name
            ),
            scores=[ScoreBase(
                name=score.name,
                score=score.score
            ) for score in report.scores],
            timestamp=report.timestamp
        ) for report in website.reports]

    # return a website item by its url
    def get_by_url(self, db: Session, *, url: str) -> Website:
        return db.query(Website).filter(Website.url == url).first()
    
website = CRUDWebsite(Website)