from __future__ import annotations
from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from typing import Optional, List


class ReportBase(BaseModel):
    """
    
    """
    notes: Optional[str]            = Field(description="Notes write by report.")
    json_report: Optional[dict]     = Field(default=None, description="Full report in JSON format.")
    start_test_timestamp: datetime  = Field(description="Start test time.")
    end_test_timestamp: datetime    = Field(description="End test time.")

class ReportTool(BaseModel):
    """
    """
    name: str = Field(description="Tool's name.")
    type: str = Field(description="Tool's type.")

class ReportScore(BaseModel):
    """
    """
    name: str   = Field(description="Score's name.")
    score: int  = Field(description="One of the score of the report.")

# class to create a new Report and return via API
class ReportCreate(ReportBase):
    """
    """
    tool: ReportTool                    = Field(description="Info about report's tool.")
    scores: Optional[List[ReportScore]] = Field(default=None, description="All scores of the report.")
    url: str                            = Field(description="Website which was tested on.")


# ...
class ReportUpdate(ReportBase):
    """
    """
    tool: Optional[ReportScore]     = Field(description="", default=None)
    scores: Optional[ReportTool]    = Field(description="", default=None)


# class to return all scores data from API
class ReportScoresOutput(BaseModel):
    """
    """
    id: UUID4                   = Field(description="")
    tool: ReportTool            = Field(description="")
    scores: List[ReportScore]   = Field(description="")
    timestamp: datetime         = Field(description="")


# schema to return all details about a report
class ReportDetails(BaseModel):
    """
    """
    url: str                        = Field(description="")
    tool: ReportTool                = Field(description="")
    scores: List[ReportScore]       = Field(description="")
    notes: Optional[str]            = Field(description="", default=None)
    end_test_time: datetime         = Field(description="")
    test_duration_time: str         = Field(description="")
    json_report: Optional[dict]     = Field(description="")
