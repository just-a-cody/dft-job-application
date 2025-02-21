"""Data Functions that handle CRUD actions with endpoints"""

import os
import requests
import dotenv

dotenv.load_dotenv()

backend_url = os.getenv("backend_url")


def get_contacts():
    """Get all contacts from the backend"""

    response = requests.get(f"{backend_url}/contacts/", timeout=10)
    response.raise_for_status()
    return response.json()


def get_contact_by_id(contact_id: str):
    """Send GET request to /contacts"""

    response = requests.get(f"{backend_url}/contacts/{contact_id}", timeout=10)
    response.raise_for_status()
    return response.json()


def create_contact(contact):
    """Send POST request to /contacts"""

    response = requests.post(f"{backend_url}/contacts/", json=contact, timeout=10)
    response.raise_for_status()
    return response.json()


def delete_contact(contact_id: str):
    """Send DELETE request to /contacts"""

    response = requests.delete(f"{backend_url}/contacts/{contact_id}", timeout=10)
    response.raise_for_status()
    return response.json()


def update_contact(contact_id: str, contact: dict):
    """Send PUT request to /contacts"""

    response = requests.put(
        f"{backend_url}/contacts/{contact_id}", json=contact, timeout=10
    )
    response.raise_for_status()
    return response.json()
