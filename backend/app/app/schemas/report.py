from __future__ import annotations
from pydantic import BaseModel, Json
from uuid import UUID
from datetime import datetime
from typing import Optional, Any, List

from .tool import ToolBase
from .score import ScoreBase


class ReportBase(BaseModel):
    notes: Optional[str] = None
    json_report: Optional[dict] = None
    timestamp: datetime


# class to create a new Report and return via API
class ReportCreate(ReportBase):
    tool: ToolBase
    scores: Optional[List[ScoreBase]] = None
    url: str

# ...
class ReportUpdate(ReportBase):
    tool: Optional[ToolBase] = None
    scores: Optional[ScoreBase] = None


# class to return all scores data from API
class ReportScores(BaseModel):
    tool: ToolBase
    scores: List[ScoreBase]
    timestamp: datetime

    
