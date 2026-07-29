import io
import unittest
import sys
import cv2
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db
from app.db.models import User, Prediction
from app.services.recommendation_service import RecommendationService
from app.ai.preprocess import preprocess_image
from app.ai.model_loader import model_loader
from app.ai.predictor import predictor


class TestModule1(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.db = Session()

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(bind=self.engine)

    def test_user_and_prediction_models(self):
        user = User(
            email="farmer@farmguard.ai",
            hashed_password="hashed_secret_password",
            full_name="Farmer John"
        )
        self.db.add(user)
        self.db.commit()

        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "farmer@farmguard.ai")

        prediction = Prediction(
            user_id=user.id,
            crop="Tomato",
            disease="Tomato Late Blight",
            confidence=0.974,
            inference_time=0.042,
            image_path="uploads/test_tomato.jpg"
        )
        self.db.add(prediction)
        self.db.commit()

        self.assertIsNotNone(prediction.id)

    def test_recommendation_service(self):
        service = RecommendationService()
        supported = service.list_supported_diseases()
        self.assertEqual(len(supported), 8)


class TestModule2Auth(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

        def override_get_db():
            db = TestingSessionLocal()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=self.engine)

    def test_successful_registration(self):
        resp = self.client.post(
            "/api/v1/register",
            json={"email": "newfarmer@farmguard.ai", "password": "securepassword123", "full_name": "New Farmer"}
        )
        self.assertEqual(resp.status_code, 201)


class TestModule3AI(unittest.TestCase):
    def setUp(self):
        img = np.zeros((300, 300, 3), dtype=np.uint8)
        img[:, :, 1] = 180
        _, buffer = cv2.imencode('.jpg', img)
        self.image_bytes = buffer.tobytes()

    def test_disease_predictor(self):
        result = predictor.predict(self.image_bytes)
        self.assertIn("crop", result)
        self.assertIn("disease", result)


class TestModule4PredictAndHistory(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

        def override_get_db():
            db = TestingSessionLocal()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=self.engine)

    def _get_token(self):
        self.client.post(
            "/api/v1/register",
            json={"email": "tester@farmguard.ai", "password": "password123"}
        )
        resp = self.client.post(
            "/api/v1/login",
            json={"email": "tester@farmguard.ai", "password": "password123"}
        )
        return resp.json()["access_token"]

    def _make_file(self):
        img = np.zeros((300, 300, 3), dtype=np.uint8)
        img[:, :, 1] = 180
        _, buffer = cv2.imencode('.jpg', img)
        return ("test_leaf.jpg", io.BytesIO(buffer.tobytes()), "image/jpeg")

    def test_predict_endpoint_flow(self):
        token = self._get_token()
        resp = self.client.post(
            "/api/v1/predict",
            files={"file": self._make_file()},
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(resp.status_code, 201)


class TestModule5Dashboard(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

        def override_get_db():
            db = TestingSessionLocal()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=self.engine)

    def _get_token(self):
        self.client.post(
            "/api/v1/register",
            json={"email": "dash_test@farmguard.ai", "password": "password123"}
        )
        resp = self.client.post(
            "/api/v1/login",
            json={"email": "dash_test@farmguard.ai", "password": "password123"}
        )
        return resp.json()["access_token"]

    def test_dashboard_endpoint_flow(self):
        token = self._get_token()
        resp = self.client.get(
            "/api/v1/dashboard",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("total_scans", data)
        self.assertIn("crop_distribution", data)
        self.assertIn("disease_distribution", data)
        self.assertIn("recent_scans", data)

if __name__ == "__main__":
    unittest.main()
