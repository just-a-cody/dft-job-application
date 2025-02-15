from core.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, String
from datetime import datetime
import uuid


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    def __repr__(self) -> str:
        return f"<Contact: {self.name} created at {self.created_at}>"
