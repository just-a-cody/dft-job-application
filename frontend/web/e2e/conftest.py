"""Conftest file for E2E tests"""

import os
import re
from typing import Generator

import dotenv
import pytest
from faker import Faker
from playwright.sync_api import APIRequestContext, Playwright

fake = Faker(["en_GB"])

dotenv.load_dotenv()


@pytest.fixture(scope="session")
def frontend_url():
    """Fixture for getting frontend URL"""

    return os.getenv("frontend_url") or "http://localhost:8000"


@pytest.fixture(scope="session")
def backend_url():
    """Fixture for getting backend URL"""

    return os.getenv("backend_url") or "http://localhost:8001"


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    """Fixture for getting API request context"""

    headers = {
        "Accept": "application/json",
    }
    request_context = playwright.request.new_context(extra_http_headers=headers)
    yield request_context
    request_context.dispose()


@pytest.fixture
def contact_cleanup():
    created_contacts = []

    def _create_contact(api_request_context, backend_url):
        user = {
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address(),
            "phone": re.sub(r"\D", "", fake.phone_number()),
        }
        res = api_request_context.post(f"{backend_url}/contacts", data=user)
        contact = res.json()
        created_contacts.append((api_request_context, backend_url, contact["id"]))
        return contact

    yield _create_contact

    # Teardown: Clean up all created contacts
    for api_context, backend_url, contact_id in created_contacts:
        try:
            api_context.delete(f"{backend_url}/contacts/{contact_id}")
        except Exception as e:
            print(f"Failed to delete contact {contact_id}: {e}")
