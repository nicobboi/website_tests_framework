from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Union
from datetime import datetime

from .report import ReportCreate, ReportScores


class WebsiteBase(BaseModel):
    url: str = Field(description="Website's url.")


class WebsiteCreate(WebsiteBase):
    reports: Optional[List[ReportCreate]] = Field(default=None, description="All reports of the tests on the website.")

class WebsiteUpdate(WebsiteBase):
    reports: List[ReportCreate] = Field(description="All reports of the tests on the website.")


class WebsiteRun(WebsiteBase):
    test_types: List[str] = Field(description="List of test's types to launch on website.")


class WebsiteSchedule(WebsiteRun):
    crontab: str = Field(description="Crontab string for scheduling task.")



class WebsiteReportsScores(WebsiteBase):
    reports_scores: List[ReportScores] = Field(description="All reports scores of this website.")

class AllWebsiteScores(WebsiteBase):
    site_id: UUID4 = Field(description="Website's id in the database.")
    scores: Dict[str, Union[int, None]] = Field(description="Schema used for passing scores of all website in the db.")