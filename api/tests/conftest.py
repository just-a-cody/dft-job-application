import pytest
from fastapi.testclient import TestClient
from main import app
from core.db import get_test_session, get_session, test_engine
from schemas.contact import Base


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[get_session] = get_test_session
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def setup_database(override_dependency):  # for the order of execution
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
