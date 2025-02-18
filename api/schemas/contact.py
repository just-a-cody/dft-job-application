"""Sqlalchemy schemas for contact model"""

import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, MappedAsDataclass
from sqlalchemy import Text, String, func


class Base(MappedAsDataclass, DeclarativeBase):
    """Base class for all models"""


class Contact(Base):
    """Contact sqlalchemy model"""

    __tablename__ = "contacts"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(32), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default_factory=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    def __repr__(self) -> str:
        return f"<Contact: {self.name} created at {self.created_at}>"
