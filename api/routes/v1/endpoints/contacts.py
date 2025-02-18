"""Endpoints for contacts"""

from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from services.contact import ContactService
from core.db import get_session
from models.contact import ContactModel, InsertContactModel
from models.errors import ErrorModel, DatabaseOperationError

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
            "model": ErrorModel,
        },
    },
)

Service = Annotated[ContactService, Depends(ContactService)]
DBSession = Annotated[Session, Depends(get_session)]


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
def contact_list(service: Service, session: DBSession):
    """List all contacts endpoint"""
    try:
        contacts = service.get_all_contacts(session)
        return contacts
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@router.post(
    "/",
    description="Create new contact",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Successfully created new contact",
            "model": ContactModel,
        },
    },
)
def create_contact(
    service: Service, contact_data: InsertContactModel, session: DBSession
):
    """Create a new contact endpoint"""
    try:
        new_contact = service.create_contact(contact_data, session)
        return new_contact
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
