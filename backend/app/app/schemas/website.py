from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Union
from enum import Enum
from .report import ReportCreate, ReportScoresOutput


class TestTypes(str, Enum):
    accessibility = "accessibility"
    performance = "performance"
    security = "security"
    seo = "seo"
    validation = "validation"


class WebsiteBase(BaseModel):
    url: str = Field(description="Website's url.")

class WebsiteCreate(WebsiteBase):
    reports: Optional[List[ReportCreate]] = Field(default=None, description="All reports of the tests on the website.")

class WebsiteUpdate(WebsiteBase):
    reports: List[ReportCreate] = Field(description="All reports of the tests on the website.")



class WebsiteRun(WebsiteBase):
    test_types: List[TestTypes] = Field(description="List of test's types to launch on website.")

class WebsiteReportsScores(WebsiteBase):
    reports_scores: List[ReportScoresOutput] = Field(description="All reports scores of this website.")

class AllWebsiteScores(WebsiteBase):
    site_id: UUID4 = Field(description="Website's id in the database.")
    scores: Dict[str, Union[int, None]] = Field(description="Schema used for passing scores of all website in the db.")
