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


def create_contact(contact):
    """Send POST request to /contacts"""

    response = requests.post(f"{backend_url}/contacts/", json=contact, timeout=10)
    response.raise_for_status()
    return response.json()
