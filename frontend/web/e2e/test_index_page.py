import re
from playwright.sync_api import Page, expect


def test_index_page_has_correct_title(page: Page, frontend_url: str):
    page.goto(frontend_url)
    expect(page).to_have_title(re.compile(r".*UK Government Contact Book"))


def test_index_page_has_correct_header(page: Page, frontend_url: str):
    page.goto(frontend_url)
    expect(page.get_by_role("heading", name="UK Government Contact Book")).to_be_visible()


def test_contact_created_success_message(page: Page, frontend_url: str):
    page.goto(f"{frontend_url}/?message=contact-created-success")
    expect(page.get_by_role("alert", name="message-box")).to_have_text(
        "successfully created new contact", ignore_case=True
    )


def test_random_message_should_not_be_shown(page: Page, frontend_url: str):
    page.goto(f"{frontend_url}/?message=random-message")
    expect(page.get_by_role("alert", name="message-box")).not_to_be_visible()
