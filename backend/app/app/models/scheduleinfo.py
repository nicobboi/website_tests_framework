from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import String, Time
from datetime import time, timezone
from uuid import uuid4

from enum import Enum

from app.db.base_class import Base

if TYPE_CHECKING:
    from .schedule import Schedule


class DaysEnum(str, Enum):
    """
    Enum class to validate days attribute
    """
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class ScheduleInfo(Base):
    id:         Mapped[UUID]            = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    time:       Mapped[Time]            = mapped_column(Time(timezone=True), nullable=False, server_default=str(time(hour=0, minute=0, tzinfo=timezone.utc)))
    days:       Mapped[ARRAY(String)]   = mapped_column(MutableList.as_mutable(ARRAY(String)), nullable=False, server_default=str([]))

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
    @validates("day")
    def validate_day(self, key, value):
        for day in value:
            if not day in (DaysEnum).__members__.values():
                raise ValueError(f'Invalid hour: {value}')
        return value

    schedules:          Mapped[list["Schedule"]]        = relationship(back_populates="schedule_info", cascade="all, delete, delete-orphan")