import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def mock_firebase():
    with patch('app.config.init_firebase'):
        yield


@pytest.fixture
def mock_auth():
    with patch('firebase_admin.auth.verify_id_token') as mock_verify:
        mock_verify.return_value = {
            'uid': 'test-user-id',
            'email': 'test@example.com',
            'name': 'Test User'
        }
        yield mock_verify


@pytest.fixture
def mock_repo():
    with patch('app.repositories.firestore.repo') as mock:
        mock.get_user = AsyncMock(return_value=None)
        mock.create_user = AsyncMock()
        mock.create_group = AsyncMock()
        mock.get_group = AsyncMock()
        mock.update_group = AsyncMock()
        mock.delete_group = AsyncMock()
        mock.list_user_groups = AsyncMock(return_value=[])
        mock.add_member_to_group = AsyncMock()
        mock.remove_member_from_group = AsyncMock()
        mock.create_product = AsyncMock()
        mock.get_product = AsyncMock()
        mock.update_product = AsyncMock()
        mock.delete_product = AsyncMock()
        mock.list_group_products = AsyncMock(return_value=[])
        mock.create_chat_message = AsyncMock()
        mock.list_group_messages = AsyncMock(return_value=[])
        yield mock


@pytest.fixture
def client(mock_firebase, mock_auth):
    return TestClient(app)


@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-token"}
