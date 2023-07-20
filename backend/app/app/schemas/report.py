from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any, List

from .tool import ToolBase
from .score import ScoreBase


class ReportBase(BaseModel):
    notes: Optional[str] = Field(description="Notes write by report.")
    json_report: Optional[dict] = Field(default=None, description="Full report in JSON format.")
    start_test_timestamp: datetime = Field(description="Start test time.")
    end_test_timestamp: datetime = Field(description="End test time.")


# class to create a new Report and return via API
class ReportCreate(ReportBase):
    tool: ToolBase = Field(description="Info about report's tool.")
    scores: Optional[List[ScoreBase]] = Field(default=None, description="All scores of the report.")
    url: str = Field(description="Website which was tested on.")


# ...
class ReportUpdate(ReportBase):
    tool: Optional[ToolBase] = None
    scores: Optional[ScoreBase] = None


# class to return all scores data from API
class ReportScores(BaseModel):
    tool: ToolBase
    scores: List[ScoreBase]
    timestamp: datetime


# schema to return all details about a report
class ReportDetails(BaseModel):
    url: str
    tool: ToolBase
    scores: List[ScoreBase]
    notes: Optional[str] = None
    end_test_time: datetime
    test_duration_time: str
    json_report: Optional[dict]
