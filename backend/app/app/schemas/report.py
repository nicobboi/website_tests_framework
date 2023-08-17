from __future__ import annotations
from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from typing import Optional, List


class ReportBase(BaseModel):
    """
    Base class for Report model validation
    """
    notes: Optional[str]            = Field(description="Notes write by report.")
    json_report: Optional[dict]     = Field(default=None, description="Full report in JSON format.")
    start_test_timestamp: datetime  = Field(description="Start test time.")
    end_test_timestamp: datetime    = Field(description="End test time.")

class ReportTool(BaseModel):
    """
    Class to handle report's tool validation
    """
    name: str = Field(description="Tool's name.")
    type: str = Field(description="Tool's type.")

class ReportScore(BaseModel):
    """
    Class to handle one of report's score validation
    """
    name: str   = Field(description="Score's name.")
    score: int  = Field(description="One of the score of the report.")

class ReportCreate(ReportBase):
    """
    Class to handle creation of Report model
    """
    tool: ReportTool                    = Field(description="Info about report's tool.")
    scores: Optional[List[ReportScore]] = Field(default=None, description="All scores of the report.")
    url: str                            = Field(description="Website which was tested on.")

class ReportUpdate(ReportBase):
    """
    Class to handle update of Report model
    """
    tool: Optional[ReportScore]     = Field(description="Info about report's tool.", default=None)
    scores: Optional[ReportTool]    = Field(description="All scores of the report.", default=None)



class ReportScoresOutput(BaseModel):
    """
    Class to return all scores data from API
    """
    id: UUID4                   = Field(description="Report ID")
    tool: ReportTool            = Field(description="Report tool info")
    scores: List[ReportScore]   = Field(description="All report scores")
    timestamp: datetime         = Field(description="End test time")

class ReportDetails(BaseModel):
    """
    Class to return all details about a report
    """
    url: str                        = Field(description="Url tested")
    tool: ReportTool                = Field(description="Report tool info")
    scores: List[ReportScore]       = Field(description="All report scores")
    notes: Optional[str]            = Field(description="Report notes", default=None)
    end_test_time: datetime         = Field(description="End test time")
    test_duration_time: str         = Field(description="Test time duration")
    json_report: Optional[dict]     = Field(description="Full report with all the data")
