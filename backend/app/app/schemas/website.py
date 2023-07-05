from pydantic import BaseModel
from typing import List, Optional

from .report import ReportCreate


class WebsiteBase(BaseModel):
    url: str


class WebsiteCreate(WebsiteBase):
    reports: Optional[List[ReportCreate]] = None

class WebsiteUpdate(WebsiteBase):
    reports: List[ReportCreate]

