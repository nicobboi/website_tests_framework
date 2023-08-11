from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from app.db.base_class import Base

if TYPE_CHECKING:
    from .schedule import Schedule

class ScheduleInfo(Base):
    id:                 Mapped[UUID]                = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    min:                Mapped[int]                 = mapped_column(nullable=True, default=None)
    hour:               Mapped[int]                 = mapped_column(nullable=True, default=None)

    @validates("min")
    def validate_min(self, key, value):
        if not 0 <= value <= 60:
            raise ValueError(f'Invalid minute: {value}')
        return value
    @validates("hour")
    def validate_min(self, key, value):
        if not 0 <= value <= 24:
            raise ValueError(f'Invalid hour: {value}')
        return value

    schedules:        Mapped[list["Schedule"]]      = relationship(back_populates="schedules", cascade="all, delete, delete-orphan")