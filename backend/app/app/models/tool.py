from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import UniqueConstraint
from uuid import uuid4

from app.db.base_class import Base

if TYPE_CHECKING:
    from .report import Report

class Tool(Base):
    id:         Mapped[UUID]        = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name:       Mapped[str]         = mapped_column(nullable=False)
    type:       Mapped[str]         = mapped_column(nullable=False)

    reports:    Mapped[list["Report"]]    = relationship(back_populates="tool")

    UniqueConstraint(name)