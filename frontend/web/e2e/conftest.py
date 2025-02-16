import pytest
import os
import dotenv

dotenv.load_dotenv()


@pytest.fixture(scope="session")
def url():
    return os.getenv("frontend_url") or "http://localhost:8000"
