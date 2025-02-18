"""Fixtures for API tests"""

import pytest
from fastapi.testclient import TestClient
from main import app
from core.db import get_test_session, get_session, test_engine
from schemas.contact import Base


@pytest.fixture
def client() -> TestClient:
    """Test client fixture for API unit tests"""

    return TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """
    Automatically setup the database for the unit tests. Make sure it uses the test session
    and handle the creation and dropping of tables during the tests
    """

    app.dependency_overrides[get_session] = get_test_session
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.clear()
