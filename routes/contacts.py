from fastapi import APIRouter, HTTPException, status
from models.contact import Contact

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
)

@router.get("/", description="Get all contacts")
async def contact_list() -> list[Contact]:
    pass

@router.post("/", description="Create a new contact")
async def create_contact(contact: Contact) -> Contact:
    pass

@router.get("/{contact_id}", description="Get a contact by ID", responses={status.HTTP_404_NOT_FOUND: {"description": "Contact not found with the given ID"}, status.HTTP_200_OK: {"description": "Contact found"}})
async def get_contact(contact_id: int) -> Contact:
    pass

@router.put("/{contact_id}", description="Update a contact by ID", responses={status.HTTP_404_NOT_FOUND: {"description": "Contact not found with the given ID"}, status.HTTP_202_ACCEPTED: {"description": "Contact updated"}})
async def update_contact(contact_id: int) -> Contact:
    pass

@router.delete("/{contact_id}", description="Delete a contact by ID", responses={status.HTTP_404_NOT_FOUND: {"description": "Contact not found with the given ID"}, status.HTTP_202_ACCEPTED: {"description": "Contact deleted"}})
async def delete_contact(contact_id: int) -> Contact:
    pass