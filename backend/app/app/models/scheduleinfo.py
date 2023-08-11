from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, Column, ForeignKey
from uuid import uuid4

from enum import Enum

from app.db.base_class import Base

if TYPE_CHECKING:
    from .schedule import Schedule

scheduleinfo_day_relation_table = Table(
    "scheduleinfo_day",
    Base.metadata,
    Column("id", UUID, primary_key=True, index=True, default=uuid4),
    Column("scheduleinfo_id", UUID, ForeignKey("scheduleinfo.id")),
    Column("scheduleday_id", UUID, ForeignKey("scheduleday.id")),
)


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

    schedules:          Mapped[list["Schedule"]]        = relationship(back_populates="schedules", cascade="all, delete, delete-orphan")
    days:               Mapped[list["ScheduleDay"]]     = relationship(secondary=scheduleinfo_day_relation_table, back_populates="schedules")


class DaysEnum(str, Enum):
    """
    Enum class to validate day attribute in scheduleday entity
    """
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"

class ScheduleDay(Base):
    id:     Mapped[UUID]    = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    day:    Mapped[str]     = mapped_column(nullable=False)   

    @validates("day")
    def validate_day(self, key, value):
        if not value in (DaysEnum).__members__.values():
            raise ValueError(f'Invalid hour: {value}')
        return value
    
    schedules:   Mapped[list["Schedule"]]       = relationship(secondary=scheduleinfo_day_relation_table, back_populates="days")