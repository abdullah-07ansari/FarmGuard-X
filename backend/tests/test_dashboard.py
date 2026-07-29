import io
import cv2
import numpy as np
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


def create_test_image_file():
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    img[:, :, 1] = 200  # Green
    _, buffer = cv2.imencode('.jpg', img)
    return ("leaf_test.jpg", io.BytesIO(buffer.tobytes()), "image/jpeg")


def get_auth_token(client):
    client.post(
        "/api/v1/register",
        json={"email": "dash_user@farmguard.ai", "password": "password123", "full_name": "Dashboard User"}
    )
    resp = client.post(
        "/api/v1/login",
        json={"email": "dash_user@farmguard.ai", "password": "password123"}
    )
    return resp.json()["access_token"]


def test_dashboard_empty_user(client):
    token = get_auth_token(client)
    resp = client.get("/api/v1/dashboard", headers={"Authorization": f"Bearer {token}"})
    
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_scans"] == 0
    assert data["healthy_count"] == 0
    assert data["diseased_count"] == 0
    assert data["healthy_percentage"] == 0.0
    assert len(data["recent_scans"]) == 0


def test_dashboard_with_scans(client):
    token = get_auth_token(client)

    # Perform scans
    client.post(
        "/api/v1/predict",
        files={"file": create_test_image_file()},
        headers={"Authorization": f"Bearer {token}"}
    )

    resp = client.get("/api/v1/dashboard", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()

    assert data["total_scans"] == 1
    assert len(data["crop_distribution"]) >= 1
    assert len(data["recent_scans"]) == 1
    assert "recommendation" in data["recent_scans"][0]


def test_unauthenticated_dashboard(client):
    resp = client.get("/api/v1/dashboard")
    assert resp.status_code == 401
