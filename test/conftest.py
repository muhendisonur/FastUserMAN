import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from database.models import Base
from services.user_service import UserService
from main import app
from routes.user_routes import get_session
from schemas.User import User

from fastapi.testclient import TestClient


test_engine = create_engine(
    "sqlite:///:memory:", 
    echo=True,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
    )
Session = sessionmaker(test_engine)


@pytest.fixture(scope="function")
def test_client_with_5_data():
    Base.metadata.create_all(test_engine)

    def get_test_service_with_5_data():
        try:
            session = Session()
            service = UserService(session)
            service.insert_user("onur", "onur@ben.com", 25)
            service.insert_user("ahmet", "ahmet@mehmet.com", 48)
            service.insert_user("jack", "jac@jack.com", 30)
            service.insert_user("hasan", "hasan@hasan.com", 16)
            service.insert_user("turkish", "turkish@ben.com", 18)
            yield service
        finally:
            session.close()
    
    app.dependency_overrides[get_session] = get_test_service_with_5_data        
    client = TestClient(app)
    yield client

    Base.metadata.drop_all(test_engine)

@pytest.fixture(scope="function")
def test_client_without_data():
    Base.metadata.create_all(test_engine)

    def get_test_service_without_data():
        try:
            session = Session()
            yield UserService(session)
        finally:
            session.close()
    
    app.dependency_overrides[get_session] = get_test_service_without_data      
    client = TestClient(app)
    yield client

    Base.metadata.drop_all(test_engine)
    

class MockUserService:
    def get_user_by_id() -> User:
        return User(user_id=1, name="onur", email="ben@onur.com", age=24)


