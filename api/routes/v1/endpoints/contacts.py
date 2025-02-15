from fastapi import APIRouter, status, Depends, HTTPException
from services.contact import ContactService
from core.db import get_session
from models.contact import ContactModel
from models.errors import ErrorModel
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
)


@router.get(
    "/",
    description="Get all contacts",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Return the list of contacts",
            "model": list[ContactModel],
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
            "model": ErrorModel,
        },
    },
)
def contact_list(
    service: Annotated[ContactService, Depends(ContactService)],
    db: Annotated[Session, Depends(get_session)],
):
    try:
        contacts = service.get_all_contacts(db)
        return contacts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
