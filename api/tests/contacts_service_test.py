"""Unit tests for contacts service"""

from uuid import uuid4
import pytest
from services.contact import ContactService
from schemas.contact import Contact
from models.errors import DatabaseOperationError
from models.contact import InsertContactModel
from faker import Faker

FAKE_ERROR_MESSAGE = Faker().sentence()
FAKE_NAME = Faker().name()
FAKE_ADDRESS = Faker().address()
FAKE_NUMBER = Faker().phone_number()
FAKE_EMAIL = Faker().email()


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
        mock_session.scalars.side_effect = Exception(FAKE_ERROR_MESSAGE)

        with pytest.raises(DatabaseOperationError) as e:
            service.get_all_contacts(mock_session)

        assert e.value.args[0] == f"Failed to get all contacts: {FAKE_ERROR_MESSAGE}"


class TestGetContactById:
    """Test class for get_contact_by_id service"""

    def test_get_contact_by_id(self, mocker):
        """Should return the contact"""

        fake_contact = Contact(
            id=1,
            name=FAKE_NAME,
            address=FAKE_ADDRESS,
            email=FAKE_EMAIL,
            phone=FAKE_NUMBER,
        )

        service = ContactService()
        mock_session = mocker.Mock()
        mock_session.scalars.return_value.one_or_none.return_value = fake_contact

        result = service.get_contact_by_id(1, mock_session)
        assert result == fake_contact.__dict__

    def test_handle_db_error(self, mocker):
        """Should throw database operation error"""
        service = ContactService()
        mock_session = mocker.Mock()
        mock_session.scalars.side_effect = Exception(FAKE_ERROR_MESSAGE)

        with pytest.raises(DatabaseOperationError) as e:
            service.get_contact_by_id(1, mock_session)

        mock_session.scalars.assert_called_once()
        mock_session.commit.assert_not_called()
        assert e.value.args[0] == f"Failed to get contact by id: {FAKE_ERROR_MESSAGE}"

    def test_handle_not_found_error(self, mocker):
        """Should throw database not found error"""
        service = ContactService()
        mock_session = mocker.Mock()
        mock_session.scalars.return_value.one_or_none.return_value = None

        response = service.get_contact_by_id(1, mock_session)
        assert response is None


class TestCreateContact:
    """Test class for create_contact service"""

    def test_create_contact(self, mocker):
        """
        Should return the new contact
        """
        service = ContactService()
        new_data = InsertContactModel(
            name=FAKE_NAME,
            address=FAKE_ADDRESS,
            email=FAKE_EMAIL,
            phone=FAKE_NUMBER,
        )
        mock_session = mocker.Mock()

        result = service.create_contact(new_data, mock_session)

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.flush.assert_called_once()
        assert result.name == new_data.name
        assert result.address == new_data.address

    def test_handle_db_error(self, mocker):
        """
        Should throw database operation error
        """
        service = ContactService()
        new_data = InsertContactModel(
            name=FAKE_NAME,
            address=FAKE_ADDRESS,
            email=FAKE_EMAIL,
            phone=FAKE_NUMBER,
        )
        mock_session = mocker.Mock()
        mock_session.commit.side_effect = Exception(FAKE_ERROR_MESSAGE)

        with pytest.raises(DatabaseOperationError) as e:
            service.create_contact(new_data, mock_session)

        mock_session.add.assert_called_once()
        mock_session.flush.assert_not_called()
        mock_session.rollback.assert_called_once()
        assert e.value.args[0] == f"Failed to create new contact: {FAKE_ERROR_MESSAGE}"


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

    def test_handle_db_error(self, mocker):
        """
        Should throw database operation error
        """
        service = ContactService()
        fake_contact_id = uuid4()

        mock_session = mocker.Mock()
        mock_session.commit.side_effect = Exception(FAKE_ERROR_MESSAGE)

        with pytest.raises(DatabaseOperationError) as e:
            service.delete_contact(contact_id=fake_contact_id, session=mock_session)

        mock_session.rollback.assert_called_once()
        assert e.value.args[0] == f"Failed to delete a contact: {FAKE_ERROR_MESSAGE}"

    def test_handle_not_found_error(self, mocker):
        """Should throw database not found error"""
        service = ContactService()
        fake_contact_id = uuid4()

        mock_session = mocker.Mock()
        mock_session.scalars.return_value.one_or_none.return_value = None

        response = service.delete_contact(
            contact_id=fake_contact_id, session=mock_session
        )

        mock_session.rollback.assert_not_called()
        assert response is None


class TestUpdateContact:
    """Test class for update_contact service"""

    def test_update_contact(self, mocker):
        """Should return the updated contact"""
        service = ContactService()
        fake_contact_id = uuid4()
        fake_insert_contact = InsertContactModel(
            address=FAKE_ADDRESS,
            email=FAKE_EMAIL,
            name=FAKE_NAME,
            phone=FAKE_NUMBER,
        )

        mock_session = mocker.Mock()
        mock_session.scalars.return_value.one_or_none.return_value = Contact(
            id=fake_contact_id,
            address=FAKE_ADDRESS,
            email=FAKE_EMAIL,
            name=FAKE_NAME,
            phone=FAKE_NUMBER,
        )

        result = service.update_contact(
            contact_id=fake_contact_id,
            update_data=fake_insert_contact,
            session=mock_session,
        )
        mock_session.commit.assert_called_once()
        mock_session.rollback.assert_not_called()
        assert result["name"] == fake_insert_contact.name
        assert result["id"] == fake_contact_id
        assert result["email"] == fake_insert_contact.email

    def test_handle_db_error(self, mocker):
        """Should throw database operation error"""
        service = ContactService()
        fake_contact_id = uuid4()
        fake_insert_contact = InsertContactModel(
            address=FAKE_ADDRESS,
            email=FAKE_EMAIL,
            name=FAKE_NAME,
            phone=FAKE_NUMBER,
        )
        mock_session = mocker.Mock()
        mock_session.scalars.side_effect = Exception(FAKE_ERROR_MESSAGE)

        with pytest.raises(DatabaseOperationError) as e:
            service.update_contact(
                contact_id=fake_contact_id,
                update_data=fake_insert_contact,
                session=mock_session,
            )

        mock_session.rollback.assert_called_once()
        assert e.value.args[0] == f"Failed to update contact: {FAKE_ERROR_MESSAGE}"

    def test_handle_contact_not_found(self, mocker):
        """Should throw database not found error"""
        service = ContactService()
        fake_contact_id = uuid4()
        fake_insert_contact = InsertContactModel(
            address=FAKE_ADDRESS,
            email=FAKE_EMAIL,
            name=FAKE_NAME,
            phone=FAKE_NUMBER,
        )
        mock_session = mocker.Mock()
        mock_session.scalars.return_value.one_or_none.return_value = None

        response = service.update_contact(
            contact_id=fake_contact_id,
            update_data=fake_insert_contact,
            session=mock_session,
        )

        mock_session.rollback.assert_not_called()
        mock_session.commit.assert_not_called()
        assert response is None
