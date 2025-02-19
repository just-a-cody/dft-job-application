"""E2E tests for creating a new contact"""

import re
from playwright.sync_api import Page, expect


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


def test_form_validation(page: Page, frontend_url: str) -> None:
    """Test form validation"""

    page.goto(f"{frontend_url}/create-contact")
    page.get_by_role("textbox", name="name").fill("Somebody")
    page.get_by_role("textbox", name="email").fill("somebody@email.com")
    page.get_by_role("textbox", name="address").fill("123 High Street")
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

    page.get_by_role("textbox", name="phone").fill("1234567890")
    page.get_by_role("button", name="submit").click()
    expect(page).to_have_url(re.compile(r"/\?message=contact-created-success"))
    expect(page.get_by_role("alert", name="message-box")).to_have_text(
        "successfully created new contact", ignore_case=True
    )
