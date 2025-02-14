from fastapi import APIRouter, status, Response, Depends
from api.services.contact import ContactService
from api.db import get_session
from api.models.contact import ContactModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

router = APIRouter(
    tags=["contacts"],
)

service = ContactService()


@router.get(
    "/",
    description="Get all contacts",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Return the list of contacts",
            "model": list[ContactModel],
        },
    },
)
async def contact_list(db: Annotated[AsyncSession, Depends(get_session)]):
    contacts = await service.get_all_contacts(db)
    return contacts
