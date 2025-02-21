"""Endpoints for contacts"""

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from services.contact import ContactService
from core.db import get_session
from models.contact import ContactModel, InsertContactModel
from models.errors import ErrorModel, DatabaseOperationError, DatabaseNotFoundError

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
def contact_list_route(service: Service, session: DBSession):
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
def create_contact_route(
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


@router.delete(
    "/{contact_id}",
    description="Delete a contact by id",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_202_ACCEPTED: {
            "description": "Successfully deleted a contact",
            "model": ContactModel,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Invalid contact id",
            "model": ErrorModel,
        },
    },
)
def delete_contact_route(service: Service, contact_id: UUID, session: DBSession):
    """Delete a contact by id endpoint"""
    try:
        response = service.delete_contact(contact_id, session)

        if response is None:
            raise DatabaseNotFoundError(f"record with id {contact_id} does not exist")

        return response
    except DatabaseNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


@router.put(
    "/{contact_id}",
    description="Update a contact by id",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_202_ACCEPTED: {
            "description": "Successfully updated a contact",
            "model": ContactModel,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Invalid contact id",
            "model": ErrorModel,
        },
    },
)
def update_contact_route(
    service: Service,
    contact_id: UUID,
    contact_data: InsertContactModel,
    session: DBSession,
):
    """Update a contact by id endpoint"""
    try:
        response = service.update_contact(contact_id, contact_data, session)
        if response is None:
            raise DatabaseNotFoundError(f"record with id {contact_id} does not exist")

        return response
    except DatabaseOperationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
    except DatabaseNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
