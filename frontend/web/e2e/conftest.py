"""Conftest file for E2E tests"""

import os
import pytest
import dotenv

dotenv.load_dotenv()


@pytest.fixture(scope="session")
def frontend_url():
    """Fixture for getting frontend URL"""

    return os.getenv("frontend_url") or "http://localhost:8000"
