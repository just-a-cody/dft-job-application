from db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, String
from datetime import datetime


class Contact(Base):
    __tablename__ = "contacts"  # Fixed double underscores

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    def __repr__(self) -> str:  # Fixed double underscores
        return f"<Contact: {self.name} created at {self.created_at}>"
