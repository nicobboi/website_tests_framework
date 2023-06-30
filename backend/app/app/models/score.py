from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from uuid import uuid4

from app.db.base_class import Base

if TYPE_CHECKING:
    from .report import Report

class Score(Base):
    id:         Mapped[UUID]        = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name:       Mapped[str]         = mapped_column(nullable=False)
    score:      Mapped[int]         = mapped_column(nullable=False)
    report_id:  Mapped[UUID]        = mapped_column(UUID(as_uuid=True), ForeignKey("report.id", ondelete="CASCADE"))

    report:     Mapped["Report"]    = relationship(back_populates="scores")