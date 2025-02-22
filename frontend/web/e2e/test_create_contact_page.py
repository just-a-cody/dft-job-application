"""E2E tests for creating a new contact"""

import re
from faker import Faker
from playwright.sync_api import Page, expect, Dialog

fake = Faker(["en_GB"])


def test_navigate_from_index_page(page: Page, frontend_url: str) -> None:
    """Test navigating from index page to create contact page"""

    page.goto(frontend_url)
    create_contact_button = page.get_by_role("button", name="create contact")
    expect(create_contact_button).to_be_visible()
    create_contact_button.click()
    expect(page).to_have_url(re.compile(r".*create-contact"))


def test_form_exists(page: Page, frontend_url: str) -> None:
    """Test if the form exists on the create contact page"""

    page.goto(f"{frontend_url}/create-contact")
    expect(page.get_by_role("heading", name="create contact")).to_be_visible()
    expect(page.get_by_role("form", name="create-contact-form")).to_be_visible()


def test_contact_creation_and_deletion(page: Page, frontend_url: str) -> None:
    """Test contact creation and deletion process"""

    user = {
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "phone": re.sub(r"\D", "", fake.phone_number()),
    }

    page.goto(f"{frontend_url}/create-contact")
    page.get_by_role("textbox", name="name").fill(user["name"])
    page.get_by_role("textbox", name="email").fill(user["email"])
    page.get_by_role("textbox", name="address").fill(user["address"])
    page.get_by_role("textbox", name="phone").fill("wrong number")
    page.get_by_role("button", name="submit").click()
    expect(page.get_by_role("alert", name="form-alert")).to_have_text(
        "phone number does not match the required format", ignore_case=True
    )

    page.get_by_role("textbox", name="phone").fill("1234567")
    page.get_by_role("button", name="submit").click()
    expect(page.get_by_role("alert", name="form-alert")).to_have_text(
        "phone number does not match the required format", ignore_case=True
    )

    page.get_by_role("textbox", name="phone").fill(user["phone"])
    page.get_by_role("button", name="submit").click()
    expect(page).to_have_url(re.compile(r"/\?message=contact-created-success"))
    expect(page.get_by_role("alert", name="message-box")).to_have_text(
        "Contact created successfully.", ignore_case=True
    )
    expect(page.get_by_role("alert", name="message-box")).to_have_class(
        "alert alert-success"
    )

    expect(page.get_by_role("heading", name=user["name"], exact=True)).to_be_visible()
    expect(page.get_by_text(text=user["address"], exact=True)).to_be_visible()
    expect(page.get_by_text(text=user["email"], exact=True)).to_be_visible()
    expect(page.get_by_text(text=user["phone"], exact=True)).to_be_visible()

    def handle_dialog(dialog: Dialog):
        assert dialog.message == "Are you sure to remove this contact?"
        dialog.accept()

    page.once("dialog", handle_dialog)
    delete_btn = page.get_by_role("button", name="Delete").first
    expect(delete_btn).to_be_visible()
    delete_btn.click()

    expect(page.get_by_role("alert", name="message-box")).to_have_text(
        "Contact deleted successfully.", ignore_case=True
    )
    expect(page.get_by_role("alert", name="message-box")).to_have_class(
        "alert alert-success"
    )
    expect(
        page.get_by_role("heading", name=user["name"], exact=True)
    ).not_to_be_visible()
