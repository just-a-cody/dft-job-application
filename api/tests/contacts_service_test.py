"""Unit tests for contacts service"""

from uuid import uuid4
import pytest
from services.contact import ContactService
from schemas.contact import Contact
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


class TestDeleteService:
    """Test class for delete_contact service"""

    def test_delete_contact(self, mocker):
        """
        Should return the deleted contact
        """
        service = ContactService()

        fake_contact_id = uuid4()
        fake_contact = Contact(
            id=fake_contact_id,
            address="fake address",
            email="fake@email.com",
            name="fake name 1",
            phone="123456789",
        )

        mock_session = mocker.Mock()
        mock_session.scalars.return_value.one_or_none.return_value = fake_contact

        result = service.delete_contact(
            contact_id=fake_contact_id, session=mock_session
        )

        mock_session.commit.assert_called_once()
        assert result["name"] == "fake name 1"

    def test_handle_500_error(self, mocker):
        """
        Should throw database operation error
        """
        service = ContactService()
        fake_contact_id = uuid4()

        mock_session = mocker.Mock()
        mock_session.commit.side_effect = Exception("something wrong")

        with pytest.raises(DatabaseOperationError) as e:
            service.delete_contact(contact_id=fake_contact_id, session=mock_session)

        mock_session.rollback.assert_called_once()
        assert e.value.args[0] == "Failed to delete new contact: something wrong"

    def test_handle_404_error(self, mock):
        """Should throw database not found error"""
        pass
