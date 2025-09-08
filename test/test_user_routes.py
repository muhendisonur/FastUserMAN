from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from routes.user_routes import get_session
from main import app
from schemas.User import User


# --------------------- Integration Tests -------------------------------
def test_all_users_returns_user_list(test_client_with_5_data):
    """Test that returns is a list which is contains users"""
    response = test_client_with_5_data.get("/users")
    assert type(response.json()) == list
    
    
def test_all_users_returns_none(test_client_without_data):
    """Test if User table has any of user, returns None"""
    response = test_client_without_data.get("/users")
    assert type(response.json()) == type(None)

# --------------------- Unit Tests -------------------------------
def test_user_by_id_returns_ok_and_the_user():
    """Test user_by_id returns existing user with 200 http response code"""
    mock_user_service = MagicMock()
    fake_user = User(user_id=1, name="Onur", email="ben@onur.com", age=24)
    mock_user_service.get_user_by_id.return_value = fake_user
    
    app.dependency_overrides[get_session] = lambda: mock_user_service

    client = TestClient(app)

    response = client.get("/users/1")

    assert response.json() == fake_user.model_dump()
    assert response.status_code == 200
