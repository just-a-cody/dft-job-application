"""E2E tests for editing a contact"""

import re
import uuid
from faker import Faker
from playwright.sync_api import Page, expect, APIRequestContext

fake = Faker(["en_GB"])


def test_edit_contact(
    contact_cleanup,
    page: Page,
    frontend_url: str,
    backend_url: str,
    api_request_context: APIRequestContext,
):
    """Test editing a contact"""
    created_contact = contact_cleanup(api_request_context, backend_url)

    new_user_details = {
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "phone": re.sub(r"\D", "", fake.phone_number()),
    }

    # Navigate to and check the edit contact page
    page.goto(f"{frontend_url}/edit/{created_contact['id']}")

    expect(page.get_by_role("heading", name="edit contact")).to_be_visible()
    expect(page.get_by_role("form", name="edit-contact-form")).to_be_visible()

    # Edit the contact
    page.get_by_role("textbox", name="name").fill(new_user_details["name"])
    page.get_by_role("textbox", name="email").fill(new_user_details["email"])
    page.get_by_role("textbox", name="address").fill(new_user_details["address"])
    page.get_by_role("textbox", name="phone").fill("123")

    page.get_by_role("button", name="submit").click()

    expect(page.get_by_role("alert", name="form-alert")).to_have_text(
        "phone number does not match the required format", ignore_case=True
    )

    page.get_by_role("textbox", name="phone").fill(new_user_details["phone"])
    page.get_by_role("button", name="submit").click()

    # Check the contact is updated
    expect(page.get_by_role("alert", name="message-box")).to_have_text(
        "Contact updated successfully.", ignore_case=True
    )
    expect(page.get_by_role("alert", name="message-box")).to_have_class(
        "alert alert-success"
    )

    # Check the contact is updated
    expect(page.get_by_role("heading", name=new_user_details["name"])).to_be_visible()
    expect(page.get_by_text(new_user_details["email"])).to_be_visible()
    expect(page.get_by_text(new_user_details["address"])).to_be_visible()
    expect(page.get_by_text(new_user_details["phone"])).to_be_visible()


def test_should_prevent_invalid_contact_id(page: Page, frontend_url: str):
    """Test if the website prevent users navigate to edit page with an invalid contact id"""

    # Navigate to the edit page with an invalid contact id
    page.goto(f"{frontend_url}/edit/{uuid.uuid4()}")

    # Check the website redirects and shows an error message
    expect(page).to_have_url(f"{frontend_url}/?message=contact-not-found")
    expect(page.get_by_role("alert", name="message-box")).to_have_class(
        "alert alert-error"
    )
    expect(page.get_by_role("alert", name="message-box")).to_have_text(
        "Contact not found. Please try again.", ignore_case=True
    )
