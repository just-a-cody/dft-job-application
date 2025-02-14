from api.schemas.contact import Contact
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pprint import pprint


class ContactService:
    async def get_all_contacts(self, session: AsyncSession):  # Accept session directly
        stmt = select(Contact).order_by(Contact.created_at.desc())
        result = await session.execute(stmt)
        return result.scalars().all()
