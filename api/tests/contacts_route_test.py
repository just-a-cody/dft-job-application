"""Unit tests for contacts route"""

from uuid import uuid4
import pytest
from fastapi import HTTPException
from routes.v1.endpoints.contacts import contact_list, create_contact
from models.errors import DatabaseOperationError
from models.contact import InsertContactModel


class TestGetContactsRoute:
    """Test class for GET /contacts endpoint"""

    def test_get_contacts_route(self, mocker):
        """
        Should return a list of contacts when the service returns a list
        """
        mock_service = mocker.Mock()
        mock_service.get_all_contacts.return_value = []
        mock_get_session = mocker.Mock()

        response = contact_list(mock_service, mock_get_session)
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
            contact_list(mock_service, mock_get_session)

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

        response = create_contact(mock_service, new_data, mock_get_session)

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
            create_contact(mock_service, new_data, mock_get_session)

        mock_service.create_contact.assert_called_with(new_data, mock_get_session)
        assert e.value.status_code == 500
        assert e.value.detail == "create contact error"
