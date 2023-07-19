from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.crud.crud_tool import tool
from app.models import Website, Report
from app.schemas.website import WebsiteCreate, WebsiteUpdate, WebsiteScores
from app.schemas import ReportScores, ToolBase, ScoreBase

class CRUDWebsite(CRUDBase[Website, WebsiteCreate, WebsiteUpdate]):
    # return all websites with their latest scores
    def get_all_latest_scores(self, db: Session):
        websites = db.query(Website).all()
        output = []

        for website in websites:
            report_scores = self.get_scores(db=db, url=website.url)
            def latest_score(type):
                try:
                    sorted_timestamps = [report_score.timestamp for report_score in report_scores if report_score.tool.type == type]
                    sorted_timestamps.sort(reverse=True)
                    latest_scores = []
                    for report_score in report_scores:
                        if report_score.timestamp in sorted_timestamps[0:tool.get_no_tool_by_type(db=db, type=type)]:
                            [latest_scores.append(score.score) for score in report_score.scores if score.score != None]
                    
                    try:
                        return sum(latest_scores) / len(latest_scores)
                    except ZeroDivisionError:
                        return None
                    
                except ValueError:
                    return None

            output.append(WebsiteScores(
                url=website.url,
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
            report_scores = self.get_scores(db=db, url=website.url)
            def average_scores(type):
                import itertools
                scores_list = list(itertools.chain.from_iterable([[score_obj.score for score_obj in report_score.scores] for report_score in report_scores if report_score.tool.type == type]))
                try:
                    return sum(scores_list) / len(scores_list)
                except ZeroDivisionError:
                    return None

            
            output.append(WebsiteScores(
                url=website.url,
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
            ) for score in report.scores if score.score != None],
            timestamp=report.end_test_timestamp
        ) for report in website.reports]

    # return a website item by its url
    def get_by_url(self, db: Session, *, url: str) -> Website:
        return db.query(Website).filter(Website.url == url).first()
    
website = CRUDWebsite(Website)