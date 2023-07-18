from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Website, Report
from app.schemas.website import WebsiteCreate, WebsiteUpdate, WebsiteAverageScores
from app.schemas import ReportScores, ToolBase, ScoreBase

class CRUDWebsite(CRUDBase[Website, WebsiteCreate, WebsiteUpdate]):
    # return all website with its average scores
    def get_all_average_scores(self, db: Session):
        websites = db.query(Website).all()
        output = []

        for website in websites:
            report_scores = self.get_scores(db=db, url=website.url)
            def average_scores(type):
                import itertools
                scores_list = list(itertools.chain.from_iterable([[score_obj.score for score_obj in report_score.scores] for report_score in report_scores if report_score.tool.type == type]))
                print(scores_list)
                try:
                    return sum(scores_list) / len(scores_list)
                except ZeroDivisionError:
                    return None

            
            output.append(WebsiteAverageScores(
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
            ) for score in report.scores],
            timestamp=report.end_test_timestamp
        ) for report in website.reports]

    # return a website item by its url
    def get_by_url(self, db: Session, *, url: str) -> Website:
        return db.query(Website).filter(Website.url == url).first()
    
website = CRUDWebsite(Website)