"""Integration tests for contacts"""

from fastapi.testclient import TestClient
from pprint import pprint


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


def test_delete_contact(client: TestClient):
    """
    Should return the deleted contact
    """
    # Prepare a new contact
    new_data = {
        "name": "test123",
        "address": "fake address",
        "email": "fake@email.com",
        "phone": "1234567",
    }
    new_contact_response = client.post("/api/v1/contacts", json=new_data)
    new_contact = new_contact_response.json()

    assert "id" in new_contact

    delete_response = client.delete(
        f"/api/v1/contacts?contact_id={new_contact["id"]}",
    )
    deleted_contact = delete_response.json()

    pprint(new_contact)
    pprint(deleted_contact)

    assert delete_response.status_code == 202
    assert new_contact == deleted_contact
