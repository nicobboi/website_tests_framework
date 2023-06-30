from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, TEXT, JSON
from sqlalchemy import DateTime, ForeignKey
from uuid import uuid4
from datetime import datetime

from app.db.base_class import Base

from .website import Website
from .score import Score
from .tool import Tool

# if TYPE_CHECKING:
#     from .website import Website
#     from .score import Score
#     from .tool import Tool
    
class Report(Base):
    id:             Mapped[UUID]            = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    tool_id:        Mapped[int]             = mapped_column(UUID(as_uuid=True), ForeignKey("tool.id", ondelete="NO ACTION"))
    notes:          Mapped[Optional[TEXT]]  = mapped_column(TEXT, nullable=True)
    json_report:    Mapped[Optional[JSON]]  = mapped_column(JSON, nullable=True)
    site_id:        Mapped[UUID]            = mapped_column(UUID(as_uuid=True), ForeignKey("website.id", ondelete="CASCADE"))
    timestamp:      Mapped[datetime]        = mapped_column(DateTime, nullable=False)
    
    tool:           Mapped["Tool"]          = relationship(back_populates="reports")
    scores:         Mapped[list["Score"]]   = relationship(back_populates="report", cascade="all, delete, delete-orphan")
    website:        Mapped["Website"]       = relationship(back_populates="reports")