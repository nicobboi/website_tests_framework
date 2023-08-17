from sqlalchemy.orm import Session

from pydantic import UUID4
from typing import Optional

from app.crud.base import CRUDBase
from app import crud
from app.models import Website, Tool
from app.schemas import (
    WebsiteCreate, 
    WebsiteUpdate, 
    AllWebsiteScores, 
    WebsiteReportsScores, 
    ReportScoresOutput, 
    ReportTool, 
    ReportScore
)

class CRUDWebsite(CRUDBase[Website, WebsiteCreate, WebsiteUpdate]):
    # return all websites with their latest scores
    def get_all_latest_scores(self, db: Session):
        websites = db.query(Website).all()
        output = []

        for website in websites:
            report_scores = self.get_scores(db=db, url=website.url).reports_scores
            def latest_score(type):
                try:
                    sorted_timestamps = [report_score.timestamp for report_score in report_scores if report_score.tool.type == type]
                    sorted_timestamps.sort(reverse=True)
                    latest_scores = []
                    for report_score in report_scores:
                        if report_score.timestamp in sorted_timestamps[0:len(db.query(Tool).filter(Tool.type.has(name=type)).all())]:
                            [latest_scores.append(score.score) for score in report_score.scores]
                    
                    try:
                        return sum(latest_scores) / len(latest_scores)
                    except ZeroDivisionError:
                        return None
                    
                except ValueError:
                    return None

            output.append(AllWebsiteScores(
                url=website.url,
                site_id=website.id,
                scores={
                    'accessibility': latest_score("accessibility"),
                    'performance': latest_score("performance"),
                    'security': latest_score("security"),
                    'seo': latest_score("seo"),
                    'validation': latest_score("validation"),
                }
            ))

        return output

    # return all websites with their average scores
    def get_all_average_scores(self, db: Session):
        websites = db.query(Website).all()
        output = []

        for website in websites:
            report_scores = self.get_scores(db=db, url=website.url).reports_scores
            def average_scores(type):
                import itertools
                scores_list = list(itertools.chain.from_iterable([[score_obj.score for score_obj in report_score.scores] for report_score in report_scores if report_score.tool.type == type]))
                try:
                    return sum(scores_list) / len(scores_list)
                except ZeroDivisionError:
                    return None

            
            output.append(AllWebsiteScores(
                url=website.url,
                site_id=website.id,
                scores={
                    'accessibility': average_scores("accessibility"),
                    'performance': average_scores("performance"),
                    'security': average_scores("security"),
                    'seo': average_scores("seo"),
                    'validation': average_scores("validation"),
                }
            ))

        return output

    # return all reports scores from a given URL
    def get_scores(self, db: Session, *, url: Optional[str] = None, id: Optional[UUID4] = None):
        if url:
            website = self.get_by_url(db=db, url=url)
        elif id:
            website = self.get_by_id(db=db, id=id)
        else:
            return []
        
        if not website:
            return []

        reports = crud.report.get_all_by_website(db=db, url=website.url, timestamp_order=True)
        
        reports_scores = [ReportScoresOutput(
            id=report.id,
            tool=ReportTool(
                name=report.tool.name,
                type=report.tool.type.name
            ),
            scores=[ReportScore(
                name=score.name,
                score=score.score
            ) for score in report.scores if score.score != None],
            timestamp=report.end_test_timestamp
        ) for report in reports]

        reports_score_null = [report for report in reports_scores if not report.scores]

        for report in reports_score_null:
            reports_scores.remove(report)

        # return a refactored schema output
        return WebsiteReportsScores(
            url=website.url,
            reports_scores=reports_scores
        )

    # return a website item by its url
    def get_by_url(self, db: Session, *, url: str) -> Website:
        return db.query(Website).filter(Website.url == url).first()
    
    # return a website by its id
    def get_by_id(self, db: Session, *, id: UUID4) -> Website:
        return db.query(Website).filter(Website.id == id).first()
    
website = CRUDWebsite(Website)