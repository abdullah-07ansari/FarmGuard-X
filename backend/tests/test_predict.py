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
    img[:, :, 1] = 180  # Green leaf
    img[100:200, 100:200, 0] = 130  # Brown lesion spot
    _, buffer = cv2.imencode('.jpg', img)
    return ("leaf_test.jpg", io.BytesIO(buffer.tobytes()), "image/jpeg")


def get_auth_token(client):
    client.post(
        "/api/v1/register",
        json={"email": "predict_user@farmguard.ai", "password": "password123", "full_name": "Predict User"}
    )
    resp = client.post(
        "/api/v1/login",
        json={"email": "predict_user@farmguard.ai", "password": "password123"}
    )
    return resp.json()["access_token"]


def test_predict_endpoint_success(client):
    token = get_auth_token(client)
    file_tuple = create_test_image_file()

    response = client.post(
        "/api/v1/predict",
        files={"file": file_tuple},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()

    assert "id" in data
    assert "crop" in data
    assert "disease" in data
    assert "confidence" in data
    assert "inference_time" in data
    assert "model_version" in data
    assert "image_path" in data
    assert "recommendation" in data

    assert data["confidence"] > 0.5
    assert data["recommendation"]["crop"] == data["crop"]
    assert "symptoms" in data["recommendation"]
    assert "organic_treatment" in data["recommendation"]
    assert "chemical_treatment" in data["recommendation"]


def test_history_endpoint_success(client):
    token = get_auth_token(client)
    file_tuple = create_test_image_file()

    # Upload 2 scans
    client.post("/api/v1/predict", files={"file": file_tuple}, headers={"Authorization": f"Bearer {token}"})
    client.post("/api/v1/predict", files={"file": file_tuple}, headers={"Authorization": f"Bearer {token}"})

    # Fetch History
    response = client.get("/api/v1/history", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 2
    assert "recommendation" in data["items"][0]


def test_unauthenticated_predict(client):
    file_tuple = create_test_image_file()
    response = client.post("/api/v1/predict", files={"file": file_tuple})
    assert response.status_code == 401
