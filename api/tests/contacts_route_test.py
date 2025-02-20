"""Unit tests for contacts route"""

from uuid import uuid4
import pytest
from fastapi import HTTPException
from routes.v1.endpoints.contacts import (
    contact_list_route,
    create_contact_route,
    delete_contact_route,
)
from models.errors import DatabaseOperationError
from models.contact import InsertContactModel, ContactModel


class TestGetContactsRoute:
    """Test class for GET /contacts endpoint"""

    def test_get_contacts_route(self, mocker):
        """
        Should return a list of contacts when the service returns a list
        """
        mock_service = mocker.Mock()
        mock_service.get_all_contacts.return_value = []
        mock_get_session = mocker.Mock()

        response = contact_list_route(mock_service, mock_get_session)
        mock_service.get_all_contacts.assert_called_with(mock_get_session)
        assert response == []

    def test_get_contacts_route_with_error(self, mocker):
        """
        Should raise a HTTPException when the service raises an exception
        """
        mock_service = mocker.Mock()
        mock_service.get_all_contacts.side_effect = DatabaseOperationError(
            "get contacts error"
        )
        mock_get_session = mocker.Mock()

        with pytest.raises(HTTPException) as e:
            contact_list_route(mock_service, mock_get_session)

        mock_service.get_all_contacts.assert_called_with(mock_get_session)
        assert e.value.status_code == 500
        assert e.value.detail == "get contacts error"


class TestCreateContactRoute:
    """Test class for POST /contacts endpoint"""

    def test_post_contacts_route(self, mocker):
        """
        Should return the new contact
        """
        uuid = uuid4()
        new_data = InsertContactModel(
            name="test123",
            address="fake address",
            email="fake@email.com",
            phone="1234567",
        )
        mock_service = mocker.Mock()
        mock_service.create_contact.return_value = {"id": uuid, **new_data.model_dump()}

        mock_get_session = mocker.Mock()

        response = create_contact_route(mock_service, new_data, mock_get_session)

        mock_service.create_contact.assert_called_with(new_data, mock_get_session)
        assert response["id"] == uuid
        assert response["name"] == "test123"

    def test_post_contacts_route_with_error(self, mocker):
        """
        Should return a HTTPException when the service raises an exception
        """
        new_data = InsertContactModel(
            name="test123",
            address="fake address",
            email="fake@email.com",
            phone="1234567",
        )
        mock_service = mocker.Mock()
        mock_service.create_contact.side_effect = DatabaseOperationError(
            "create contact error"
        )
        mock_get_session = mocker.Mock()

        with pytest.raises(HTTPException) as e:
            create_contact_route(mock_service, new_data, mock_get_session)

        mock_service.create_contact.assert_called_with(new_data, mock_get_session)
        assert e.value.status_code == 500
        assert e.value.detail == "create contact error"


class TestDeleteContactRoute:
    """Test class for DELETE /contacts endpoint"""

    def test_delete_contact_route(self, mocker):
        """
        Should return a HTTPException when the service raises an exception
        """
        uuid = uuid4()
        fake_deleted_contact = ContactModel(
            id=uuid,
            address="fake address",
            email="fake@email.com",
            name="Fake Name",
            phone="1234567890",
        )

        mock_service = mocker.Mock()
        mock_service.delete_contact.return_value = fake_deleted_contact
        mock_get_session = mocker.Mock()

        response = delete_contact_route(
            service=mock_service, contact_id=uuid, session=mock_get_session
        )
        mock_service.delete_contact.assert_called_with(uuid, mock_get_session)

        dumped_contact = fake_deleted_contact.model_dump()
        assert response.id == dumped_contact["id"]
        assert response.name == dumped_contact["name"]

    def test_delete_contact_route_with_500_error(self, mocker):
        """
        Should return a HTTPException when the service raises an exception
        """
        uuid = uuid4()
        mock_service = mocker.Mock()
        mock_service.delete_contact.side_effect = DatabaseOperationError(
            "delete contact error"
        )
        mock_get_session = mocker.Mock()

        with pytest.raises(HTTPException) as e:
            delete_contact_route(
                service=mock_service, contact_id=uuid, session=mock_get_session
            )
        mock_service.delete_contact.assert_called_with(uuid, mock_get_session)
        assert e.value.status_code == 500
        assert e.value.detail == "delete contact error"

    def test_delete_contact_route_with_404_error(self, mocker):
        """
        Should return a HTTPException with 404 code when the service couldn't find any record
        """
        uuid = uuid4()
        mock_service = mocker.Mock()
        mock_service.delete_contact.return_value = None

        mock_get_session = mocker.Mock()

        with pytest.raises(HTTPException) as e:
            delete_contact_route(
                service=mock_service, contact_id=uuid, session=mock_get_session
            )
        mock_service.delete_contact.assert_called_with(uuid, mock_get_session)
        assert e.value.status_code == 404
        assert e.value.detail == f"record with id {uuid} does not exist"
