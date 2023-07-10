from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from uuid import uuid4

from app.db.base_class import Base

if TYPE_CHECKING:
    from .type import Type
    from .website import Website

class Crontab(Base):
    id:             Mapped[UUID]                = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    type_id:        Mapped[UUID]                = mapped_column(UUID(as_uuid=True), ForeignKey("type.id", ondelete="CASCADE"))
    website_id:     Mapped[UUID]                = mapped_column(UUID(as_uuid=True), ForeignKey("website.id", ondelete="CASCADE"))
    active:         Mapped[bool]                = mapped_column(nullable=False)
    crontab:        Mapped[str]                 = mapped_column(nullable=False)

    website:        Mapped[Website]             = relationship(back_populates="crontabs")
    type:           Mapped[Type]                = relationship(back_populates="crontabs")