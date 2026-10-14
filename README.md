# FarmGuard X — AI Crop Pathology Platform

FarmGuard X is a production-grade, offline-first crop disease detection and agronomic advisory platform engineered to empower smallholder farmers with rapid, reliable crop diagnostics and actionable organic and chemical treatment plans.

---

## 📊 Current Project Status & Milestone Progress

> **Current Phase**: SDLC Phase 3 — ML Pipeline & Repository Stabilization Complete. Full GPU Training & Edge Quantization in Progress.

| Sprint / Milestone | Scope | Verified Evidence | Status |
|:---|:---|:---:|:---:|
| **Sprint 1: Backend MVP** | FastAPI REST API, SQLite/SQLAlchemy ORM, JWT Authentication, Diagnostics, Treatment Advisory Engine | 6/6 tests passing (`backend/tests/run_tests.py`) | ✅ **Completed** |
| **Sprint 1.5: Data Pipeline** | PlantVillage Color Subset (14,136 images, 8 classes), MD5 + dhash ($H_d \le 6$) clustering, Grouped 70/15/15 splits, Provenance | Zero-leakage verified (`split_manifest.csv`) | ✅ **Completed** |
| **Sprint 2A: Model Architecture** | MobileNetV2 transfer learning, two-phase trainer (frozen backbone $\to$ top 30 unfrozen), inverse-frequency class weights | 27/27 tests passing (`farmguard_ai/tests`) | ✅ **Completed** |
| **System Architecture & LLD** | Complete Low-Level Design (LLD), ER diagrams, API specifications, and class contracts | [`docs/LOW_LEVEL_DESIGN.md`](docs/LOW_LEVEL_DESIGN.md) | ✅ **Completed** |
| **Sprint 3B: Full Model Training** | Real-data training on full dataset (Phase 1 & Phase 2) | CPU benchmarked (27.4 img/s); GPU run pending | ⏳ **In Progress** |
| **Sprint 3C: Model Evaluation** | Held-out test evaluation, confusion matrix, macro-F1 | Scheduled post-training | 📋 **Planned** |
| **Sprint 3E: Edge Quantization** | TFLite INT8 post-training quantization ($< 15\text{ MB}$, $< 1\%$ F1 loss drop) | Configured in YAML | 📋 **Planned** |
| **Sprint 3F: Offline Mobile Inference** | On-device inference via TFLite / WebAssembly in PWA | Client UI scaffolded | 📋 **Planned** |

---

## 🛠️ Tech Stack & Architecture

- **Backend**: FastAPI, SQLAlchemy, SQLite, Pydantic v2, PyJWT, bcrypt, OpenCV
- **AI & ML Pipeline**: TensorFlow 2.21, Keras, NumPy, Pillow, PyYAML
- **Frontend / Client**: Offline-ready Progressive Web App (HTML5, Modern CSS, Vanilla JS, Service Worker)
- **Target Deployment**: MobileNetV2 INT8 quantized edge model with cloud sync

---

## 📁 Repository Blueprint

```
FarmGuard-X/
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI entry point & router registration
│   │   ├── api/routes/                 # Endpoints (auth, predict, history, dashboard)
│   │   ├── core/                       # App settings & JWT security
│   │   ├── db/                         # SQLAlchemy models (User, Prediction) & session
│   │   ├── schemas/                    # Pydantic v2 request/response schemas
│   │   ├── services/                   # Business logic & treatment database
│   │   └── ai/                         # OpenCV preprocessing & model predictor
│   └── tests/                          # Backend test suite (run_tests.py)
├── farmguard_ai/
│   ├── configs/                        # YAML experiment definitions (mobilenet_v2_int8.yaml)
│   ├── data/
│   │   └── 03_splits/                  # Portable 14,136-image split_manifest.csv
│   ├── scripts/
│   │   ├── 01_prepare_data.py          # Data acquisition, deduplication & splitting CLI
│   │   └── 02_train_model.py           # Two-phase training & CPU smoke-test CLI
│   ├── src/                            # Modular ML package (data, models, config)
│   └── tests/                          # 27 unit tests covering the ML pipeline
├── docs/
│   ├── LOW_LEVEL_DESIGN.md             # Detailed Low-Level Design (LLD) document
│   ├── PROJECT_STATE_FOR_LLM.md        # Comprehensive LLM onboarding & progress guide
│   └── project-overview.md             # High-level mission synopsis
├── index.html, app.js, sw.js           # Offline-ready client interface
└── styles.css                          # PWA responsive styling
```

---

## 🌿 The 8 Approved Pathological Classes

FarmGuard X strictly classifies and provides dual-action treatments (Organic & Chemical) for 8 Solanaceae conditions:

| ID | Class Label | Crop | Condition | Severity Tier |
|:---:|:---|:---|:---|:---:|
| `0` | `Potato___Early_blight` | Potato | Early Blight (*Alternaria solani*) | Medium |
| `1` | `Potato___Late_blight` | Potato | Late Blight (*Phytophthora infestans*) | High |
| `2` | `Potato___healthy` | Potato | Healthy / Optimal | Low |
| `3` | `Tomato___Bacterial_spot` | Tomato | Bacterial Spot (*Xanthomonas*) | High |
| `4` | `Tomato___Early_blight` | Tomato | Early Blight (*Alternaria solani*) | Medium |
| `5` | `Tomato___Late_blight` | Tomato | Late Blight (*Phytophthora infestans*) | High |
| `6` | `Tomato___Yellow_Leaf_Curl_Virus` | Tomato | TYLCV (Begomovirus / Whitefly) | Critical |
| `7` | `Tomato___healthy` | Tomato | Healthy / Optimal | Low |

---

## 🧪 Running Tests & Verification

The project includes **33 passing automated unit & integration tests** across the backend and ML pipelines:

```bash
# 1. Run the Backend test suite (6 tests)
python backend/tests/run_tests.py

# 2. Run the ML Pipeline test suite (27 tests)
python -m unittest discover -s farmguard_ai/tests -p "test_*.py"
```

---

## 🚀 Quickstart & Pipeline Execution

### 1. Launch FastAPI Backend
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# Interactive OpenAPI Swagger UI: http://localhost:8000/docs
```

### 2. Verify ML Pipeline via CPU Smoke Test
```bash
python farmguard_ai/scripts/02_train_model.py --config farmguard_ai/configs/mobilenet_v2_int8.yaml --smoke_test
```

### 3. Launch Full Training (GPU / Training Host)
```bash
python farmguard_ai/scripts/02_train_model.py --config farmguard_ai/configs/mobilenet_v2_int8.yaml --gpu_run
```

---

## 🔐 Core API Usage

### User Registration
`POST /api/v1/register`
```json
{
  "email": "farmer@farmguard.ai",
  "password": "securepassword123",
  "full_name": "Farmer John"
}
```

### User Login & Token Generation
`POST /api/v1/login`
```json
{
  "email": "farmer@farmguard.ai",
  "password": "securepassword123"
}
```

### Crop Diagnostic Scan
`POST /api/v1/predict` (Multipart form-data with image `file`)
Returns pathological condition, confidence percentage, latency, and comprehensive dual-track treatment plans (organic vs chemical) from [`recommendations.json`](backend/app/data/recommendations.json).

---

## 📖 Extended Documentation

* 📐 **Low-Level Design (LLD)**: [`docs/LOW_LEVEL_DESIGN.md`](docs/LOW_LEVEL_DESIGN.md)
* 🤖 **LLM Handoff Guide**: [`docs/PROJECT_STATE_FOR_LLM.md`](docs/PROJECT_STATE_FOR_LLM.md)
* 📋 **Project Overview**: [`docs/project-overview.md`](docs/project-overview.md)
