"""
Pytest configuration and shared fixtures for all tests
"""
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

# Set test environment
os.environ["ENV"] = "test"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.main import app
from app.db.base import Base
from app.db.session import get_db


@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    engine = create_engine(
        "sqlite:///./test.db",
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create test database session"""
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    test_session = TestSessionLocal()
    
    # Override the get_db dependency
    def override_get_db():
        try:
            yield test_session
        finally:
            test_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield test_session
    
    test_session.close()
    app.dependency_overrides.clear()


@pytest.fixture
def client(test_db):
    """Create FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def authenticated_headers(client, test_db):
    """Get authenticated headers with JWT token"""
    # Registrar user primera vez
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
    )
    
    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    return {}


@pytest.fixture
def admin_headers(client, test_db):
    """Get admin authenticated headers"""
    client.post(
        "/auth/register",
        json={
            "email": "admin@example.com",
            "password": "AdminPassword123!",
            "full_name": "Admin User",
            "role": "admin"
        }
    )
    
    response = client.post(
        "/auth/login",
        json={
            "email": "admin@example.com",
            "password": "AdminPassword123!"
        }
    )
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    return {}
