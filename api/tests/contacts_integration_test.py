from fastapi.testclient import TestClient


def test_get_contacts(client: TestClient):
    """
    Should return 200 status code and a list of contacts when the service returns a list
    """
    response = client.get("/api/v1/contacts")
    assert response.status_code == 200
    assert response.json() == []
