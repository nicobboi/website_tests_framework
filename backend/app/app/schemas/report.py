from __future__ import annotations
from pydantic import BaseModel, Json
from uuid import UUID
from datetime import datetime
from typing import Optional, Any, List

from .tool import ToolBase
from .score import ScoreBase


class ReportBase(BaseModel):
    notes: Optional[str] = None
    json_report: Optional[Json[Any]] = None
    timestamp: datetime


class ReportCreate(ReportBase):
    tool: ToolBase
    scores: List[ScoreBase]
    url: str

class ReportUpdate(ReportBase):
    tool: Optional[ToolBase] = None
    scores: Optional[ScoreBase] = None


class Report(ReportBase):
    tool: dict
    scores: list
    website: dict
    
