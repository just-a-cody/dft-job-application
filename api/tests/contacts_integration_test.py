"""Integration tests for contacts"""

from pprint import pprint
from fastapi.testclient import TestClient
from faker import Faker

BASE_CONTACT_URL = "/api/v1/contacts"


def test_get_contacts(client: TestClient):
    """
    Should return 200 status code and a list of contacts when the service returns a list
    """
    response = client.get(BASE_CONTACT_URL)
    assert response.status_code == 200
    assert response.json() == []


def test_create_contact(client: TestClient):
    """
    Should return 201 status code and the new contact
    """
    new_data = {
        "name": Faker().name(),
        "address": Faker().address(),
        "email": Faker().email(),
        "phone": Faker().phone_number(),
    }
    response = client.post(BASE_CONTACT_URL, json=new_data)

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
        "name": Faker().name(),
        "address": Faker().address(),
        "email": Faker().email(),
        "phone": Faker().phone_number(),
    }
    new_contact_response = client.post(BASE_CONTACT_URL, json=new_data)
    new_contact = new_contact_response.json()

    assert "id" in new_contact

    delete_response = client.delete(
        f"{BASE_CONTACT_URL}/{new_contact['id']}",
    )
    deleted_contact = delete_response.json()

    pprint(new_contact)
    pprint(deleted_contact)

    assert delete_response.status_code == 202
    assert new_contact == deleted_contact


def test_update_contact(client: TestClient):
    """
    Should return the updated contact
    """
    new_data = {
        "name": Faker().name(),
        "address": Faker().address(),
        "email": Faker().email(),
        "phone": Faker().phone_number(),
    }
    new_contact_response = client.post(BASE_CONTACT_URL, json=new_data)
    new_contact = new_contact_response.json()

    assert "id" in new_contact

    update_data = {
        "name": Faker().name(),
        "address": Faker().address(),
        "email": Faker().email(),
        "phone": Faker().phone_number(),
    }
    update_response = client.put(
        f"{BASE_CONTACT_URL}/{new_contact['id']}", json=update_data
    )
    updated_contact = update_response.json()

    assert update_response.status_code == 202
    assert updated_contact["id"] == new_contact["id"]
    assert updated_contact["name"] == update_data["name"]
