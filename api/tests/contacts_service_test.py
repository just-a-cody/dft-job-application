"""Unit tests for contacts service"""

import pytest
from services.contact import ContactService
from models.errors import DatabaseOperationError
from models.contact import InsertContactModel


class TestGetAllContacts:
    """Test class for get_all_contacts service"""

    def test_get_contacts(self, mocker):
        """
        Should return a list of contacts when the service returns a list
        """
        service = ContactService()
        mock_return_value = [{"id": 1, "name": "Test Contact"}]
        mock_session = mocker.Mock()
        mock_session.scalars.return_value.all.return_value = mock_return_value

        result = service.get_all_contacts(mock_session)
        assert result == mock_return_value

    def test_handle_error(self, mocker):
        """
        Should throw database operation error
        """
        service = ContactService()
        mock_session = mocker.Mock()
        mock_session.scalars.side_effect = Exception("something wrong")

        with pytest.raises(DatabaseOperationError) as e:
            service.get_all_contacts(mock_session)

        assert e.value.args[0] == "Failed to get all contacts: something wrong"


class TestCreateContact:
    """Test class for create_contact service"""

    def test_create_contact(self, mocker):
        """
        Should return the new contact
        """
        service = ContactService()
        new_data = InsertContactModel(
            name="test123",
            address="fake address",
            email="fake@email.com",
            phone="1234567",
        )
        mock_session = mocker.Mock()

        result = service.create_contact(new_data, mock_session)

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.flush.assert_called_once()
        assert result.name == new_data.name
        assert result.address == new_data.address

    def test_handle_error(self, mocker):
        """
        Should throw database operation error
        """
        service = ContactService()
        new_data = InsertContactModel(
            name="test123",
            address="fake address",
            email="fake@email.com",
            phone="1234567",
        )
        mock_session = mocker.Mock()
        mock_session.commit.side_effect = Exception("something wrong")

        with pytest.raises(DatabaseOperationError) as e:
            service.create_contact(new_data, mock_session)

        mock_session.add.assert_called_once()
        mock_session.flush.assert_not_called()
        mock_session.rollback.assert_called_once()
        assert e.value.args[0] == "Failed to create new contact: something wrong"
