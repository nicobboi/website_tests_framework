from pydantic import BaseModel, Field
from typing import List, Optional

from .report import ReportCreate


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