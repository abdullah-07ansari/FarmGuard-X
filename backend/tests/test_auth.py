import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def client():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def test_successful_registration(client):
    response = client.post(
        "/api/v1/register",
        json={"email": "newfarmer@farmguard.ai", "password": "securepassword123", "full_name": "New Farmer"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newfarmer@farmguard.ai"
    assert data["full_name"] == "New Farmer"
    assert "id" in data
    assert "hashed_password" not in data


def test_duplicate_registration(client):
    client.post(
        "/api/v1/register",
        json={"email": "duplicate@farmguard.ai", "password": "password123", "full_name": "First Registration"}
    )

    response = client.post(
        "/api/v1/register",
        json={"email": "duplicate@farmguard.ai", "password": "password456", "full_name": "Second Registration"}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_successful_login(client):
    client.post(
        "/api/v1/register",
        json={"email": "loginuser@farmguard.ai", "password": "mypassword123", "full_name": "Login User"}
    )

    response = client.post(
        "/api/v1/login",
        json={"email": "loginuser@farmguard.ai", "password": "mypassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_invalid_password_login(client):
    client.post(
        "/api/v1/register",
        json={"email": "wrongpwd@farmguard.ai", "password": "correctpassword", "full_name": "Wrong Pwd User"}
    )

    response = client.post(
        "/api/v1/login",
        json={"email": "wrongpwd@farmguard.ai", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_invalid_token_me_endpoint(client):
    response = client.get(
        "/api/v1/me",
        headers={"Authorization": "Bearer invalid_junk_token"}
    )
    assert response.status_code == 401


def test_authenticated_me_endpoint(client):
    client.post(
        "/api/v1/register",
        json={"email": "meuser@farmguard.ai", "password": "mypassword123", "full_name": "Me Profile User"}
    )
    login_resp = client.post(
        "/api/v1/login",
        json={"email": "meuser@farmguard.ai", "password": "mypassword123"}
    )
    token = login_resp.json()["access_token"]

    me_resp = client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_resp.status_code == 200
    user_data = me_resp.json()
    assert user_data["email"] == "meuser@farmguard.ai"
    assert user_data["full_name"] == "Me Profile User"
