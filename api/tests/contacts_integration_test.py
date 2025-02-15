from fastapi.testclient import TestClient


def test_get_contacts(client: TestClient):
    response = client.get("/api/v1/contacts")
    assert response.status_code == 200
    assert response.json() == []
