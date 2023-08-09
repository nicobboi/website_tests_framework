from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from datetime import datetime
from uuid import uuid4

from app.db.base_class import Base

if TYPE_CHECKING:
    from .type import Type
    from .website import Website

class Schedule(Base):
    id:                 Mapped[UUID]                = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    type_id:            Mapped[UUID]                = mapped_column(UUID(as_uuid=True), ForeignKey("type.id", ondelete="CASCADE"))
    website_id:         Mapped[UUID]                = mapped_column(UUID(as_uuid=True), ForeignKey("website.id", ondelete="CASCADE"))
    min:                Mapped[int]                 = mapped_column(nullable=True, default=None)
    hour:               Mapped[int]                 = mapped_column(nullable=True, default=None)
    day:                Mapped[int]                 = mapped_column(nullable=True, default=None)
    active:             Mapped[bool]                = mapped_column(nullable=False)
    n_run:              Mapped[int]                 = mapped_column(nullable=False, default=0)
    scheduled_time:     Mapped[datetime]            = mapped_column(nullable=True)
    last_time_launched: Mapped[datetime]            = mapped_column(nullable=True, default=None)

    website:        Mapped[Website]             = relationship(back_populates="schedules")
    type:           Mapped[Type]                = relationship(back_populates="schedules")