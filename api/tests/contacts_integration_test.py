"""Integration tests for contacts"""

from fastapi.testclient import TestClient


def test_get_contacts(client: TestClient):
    """
    Should return 200 status code and a list of contacts when the service returns a list
    """
    response = client.get("/api/v1/contacts")
    assert response.status_code == 200
    assert response.json() == []


def test_create_contact(client: TestClient):
    """
    Should return 201 status code and the new contact
    """
    new_data = {
        "name": "test123",
        "address": "fake address",
        "email": "fake@email.com",
        "phone": "1234567",
    }
    response = client.post("/api/v1/contacts", json=new_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == new_data["name"]
    assert data["address"] == new_data["address"]
    assert data["email"] == new_data["email"]
    assert data["phone"] == new_data["phone"]
    assert "id" in data
