# FarmGuard X - AI Crop Pathology Platform

FarmGuard X is a production-grade, AI-powered crop disease detection platform built as a clean, modular MVP.

---

## 🛠️ Tech Stack & Architecture

- **Backend**: FastAPI, SQLAlchemy, SQLite, Pydantic v2, PyJWT, bcrypt
- **AI Engine**: OpenCV Preprocessing + MobileNetV3 / YOLOv8-cls Classification
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS

---

## 🔐 Authentication API Usage (Module 2)

### 1. Register New User
- **Endpoint**: `POST /api/v1/register`
- **Body**:
  ```json
  {
    "email": "farmer@farmguard.ai",
    "password": "securepassword123",
    "full_name": "Farmer John"
  }
  ```
- **Response** (`201 Created`):
  ```json
  {
    "id": 1,
    "email": "farmer@farmguard.ai",
    "full_name": "Farmer John",
    "is_active": true,
    "created_at": "2026-07-29T21:50:00.000000"
  }
  ```

### 2. Login & Token Generation
- **Endpoint**: `POST /api/v1/login`
- **Body**:
  ```json
  {
    "email": "farmer@farmguard.ai",
    "password": "securepassword123"
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```

### 3. Get Current User Profile
- **Endpoint**: `GET /api/v1/me`
- **Header**: `Authorization: Bearer <access_token>`
- **Response** (`200 OK`):
  ```json
  {
    "id": 1,
    "email": "farmer@farmguard.ai",
    "full_name": "Farmer John",
    "is_active": true,
    "created_at": "2026-07-29T21:50:00.000000"
  }
  ```

---

## 🧪 Running Tests

To run the complete unit test suite for Module 1 & Module 2:

```bash
python backend/tests/run_tests.py
```
