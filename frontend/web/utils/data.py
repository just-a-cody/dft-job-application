import requests
import os
import dotenv

dotenv.load_dotenv()

backend_url = os.getenv("backend_url")


async def get_contacts():
    """
    Get all contacts from the backend
    """
    try:
        response = requests.get(f"{backend_url}/contacts/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise e
