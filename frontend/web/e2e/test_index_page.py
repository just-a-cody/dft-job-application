import re
from playwright.sync_api import Page, expect

"""
Test basic layout of the index page
"""


def test_index_page_has_correct_title(page: Page, url: str):
    page.goto(url)
    expect(page).to_have_title(re.compile("Home | UK Government Contact Book"))


def test_index_page_has_correct_header(page: Page, url: str):
    page.goto(url)
    expect(page.get_by_role("heading", name="UK Government Contact Book")).to_be_visible()


"""
Test functionalities of contact list
"""
