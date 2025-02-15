from services.contact import ContactService


def test_get_all_contacts(mocker):
    """
    Should return a list of contacts when the service returns a list
    """
    service = ContactService()
    mock_return_value = [{"id": 1, "name": "Test Contact"}]
    mock_db = mocker.Mock()
    mock_db.execute.return_value.scalars.return_value.all.return_value = mock_return_value
    service.session = mock_db
    assert service.get_all_contacts(mock_db) == mock_return_value
