from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from app.db.base_class import Base

if TYPE_CHECKING:
    from .report import Report
    from .schedule import Schedule

class Website(Base):
    id:         Mapped[UUID]            = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    url:        Mapped[str]             = mapped_column(unique=True, nullable=False)

    reports:    Mapped[list["Report"]]  = relationship(back_populates="website", cascade="all, delete, delete-orphan")
    schedules:   Mapped[list["Schedule"]] = relationship(back_populates="website", cascade="all, delete, delete-orphan")