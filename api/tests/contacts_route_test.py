from fastapi import HTTPException
from routes.v1.endpoints.contacts import contact_list
import pytest


def test_contacts_route(mocker):
    """
    Should return a list of contacts when the service returns a list
    """
    mock_service = mocker.Mock()
    mock_service.get_all_contacts.return_value = []
    mock_get_session = mocker.Mock()
    mock_get_session.return_value = mock_service

    response = contact_list(mock_service, mock_get_session)
    assert response == []


def test_contacts_route_with_error(mocker):
    """
    Should raise a HTTPException when the service raises an exception
    """
    mock_service = mocker.Mock()
    mock_service.get_all_contacts.side_effect = Exception("Test Error")
    mock_get_session = mocker.Mock()
    mock_get_session.return_value = mock_service

    with pytest.raises(HTTPException) as e:
        contact_list(mock_service, mock_get_session)

    assert e.value.status_code == 500
    assert e.value.detail == "Test Error"
