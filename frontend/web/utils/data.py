import requests
import os
import dotenv

dotenv.load_dotenv()

backend_url = os.getenv("backend_url")


async def get_contacts():
    """
    Get all contacts from the backend
    """
    response = requests.get(f"{backend_url}/contacts/")
    response.raise_for_status()
    return response.json()


async def create_contact(contact):
    """
    Create a new contact
    """
    pass


async def update_contact(contact_id, new_contact):
    """
    Update a contact
    """
    pass


async def delete_contact(contact_id):
    """
    Delete a contact
    """
    pass
