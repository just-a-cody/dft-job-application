from schemas.contact import Contact
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.errors import InternalServerException


class ContactService:
    def get_all_contacts(self, session: Session):  # Accept session directly
        stmt = select(Contact).order_by(Contact.created_at.desc())
        result = session.execute(stmt)
        return result.scalars().all()
