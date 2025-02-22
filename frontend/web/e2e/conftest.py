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


@pytest.fixture(scope="session", name="backend_url")
def backend_url_fixture():
    """Fixture for getting backend URL"""

    return os.getenv("backend_url") or "http://localhost:8001"


@pytest.fixture(scope="session", name="api_request_context")
def api_request_context_fixture(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    """Fixture for getting API request context"""

    headers = {
        "Accept": "application/json",
    }
    request_context = playwright.request.new_context(extra_http_headers=headers)
    yield request_context
    request_context.dispose()


@pytest.fixture(name="contact_id")
def contact_id_generator(api_request_context: APIRequestContext, backend_url: str):
    """Fixture for creating new user for testing and cleaning up"""

    # Before the test, create a new contact
    user = {
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "phone": re.sub(r"\D", "", fake.phone_number()),
    }

    create_response = api_request_context.post(f"{backend_url}/contacts", data=user)
    assert create_response.ok
    contact_id: str = create_response.json()["id"]

    yield contact_id

    # After the test, delete the contact
    delete_response = api_request_context.delete(f"{backend_url}/contacts/{contact_id}")
    assert delete_response.ok
