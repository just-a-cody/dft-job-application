"""Services for contact model"""

from typing import Sequence
from uuid import UUID
from sqlalchemy import select, desc, delete
from sqlalchemy.orm import Session
from schemas.contact import Contact
from models.contact import InsertContactModel
from models.errors import DatabaseOperationError


class ContactService:
    """Service for contact model"""

    def get_all_contacts(self, session: Session) -> Sequence[Contact]:
        """Get all contacts from database"""

        try:
            stmt = select(Contact).order_by(desc(Contact.created_at))
            data = session.scalars(stmt).all()
            return data
        except Exception as e:
            raise DatabaseOperationError(f"Failed to get all contacts: {str(e)}") from e

    def create_contact(self, new_contact_data: InsertContactModel, session: Session):
        """Create a new contact into database"""

        new_data = Contact(**new_contact_data.model_dump())  # to create uuid

        try:
            session.add(new_data)
            session.commit()
            session.flush()
            return new_data
        except Exception as e:
            session.rollback()
            raise DatabaseOperationError(
                f"Failed to create new contact: {str(e)}"
            ) from e

    def delete_contact(self, contact_id: UUID, session: Session):
        """Service: delete a contact by id from database"""

        stmt = delete(Contact).where(Contact.id == contact_id).returning(Contact)

        try:
            response = session.scalars(statement=stmt).one_or_none()

            if response is None:
                return None

            # copy contact to another memory slot before commiting
            deleted_contact = {**response.__dict__}
            session.commit()
            return deleted_contact
        except Exception as e:
            session.rollback()
            raise DatabaseOperationError(
                f"Failed to delete new contact: {str(e)}"
            ) from e
