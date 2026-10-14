# FarmGuard X — Comprehensive Project Progress & LLM Handoff Guide

> **Target Audience**: AI Agents / LLMs (Claude, GPT-4o, Gemini, DeepSeek, etc.) & Engineers  
> **Repository Root**: `c:\F\FarmGuard-X` (Git Branch: `main`, Remote: `https://github.com/abdullah-07ansari/FarmGuard-X`)  
> **Workspace Context**: `c:\F` contains `FarmGuard-X` (main repo) and root data/experimental caches.  
> **Current Date**: October 2026  
> **Current Phase**: Sprint 2A Completed (ML Architecture & Two-Phase Trainer verified with 100% test pass rate). Next: Sprint 2B (GPU Training & Evaluation) & Sprint 3 (INT8 Quantization).

---

## 1. Executive Project Summary

**FarmGuard X** is a production-grade, offline-first crop disease detection and agronomic treatment advisory platform engineered for rural Indian farmers. The application diagnoses plant pathology from leaf photography and immediately provides dual-track agronomic recovery plans: **Organic/Cultural** and **Chemical/Targeted**.

### Core Technical Pillars:
1. **Offline-First Edge Inference**: Fast, low-latency mobile/browser inference via INT8-quantized lightweight neural networks (MobileNetV2 / MobileNetV3) with target model size $< 15\text{ MB}$.
2. **Scientific Data Integrity & Zero Leakage**: Rigorous grouped stratified splitting with perceptual hashing (`dhash`, Hamming distance $H_d \le 6$) and MD5 checksum deduplication, guaranteeing zero cross-split data leakage.
3. **Class-Imbalanced Transfer Learning**: Custom loss weighting to resolve extreme class distribution skews ($35:1$ ratio) across 8 target classes.
4. **Full-Stack Modular MVP**: High-performance FastAPI backend with JWT security, SQLite database, static uploads, and an offline-ready PWA client.

---

## 2. Invariants & Fixed Architectural Constants

Any LLM continuing this project **must respect these non-negotiable invariants**:

### 2.1 The 8 Target Classes (`APPROVED_LABELS`)
The model is strictly trained and evaluated on 8 Solanaceae disease/healthy classes with fixed zero-indexed IDs:
| Index | Class Label | Crop | Condition | Severity Tier |
|:---:|:---|:---|:---|:---:|
| `0` | `Potato___Early_blight` | Potato | Early Blight (*Alternaria solani*) | Medium |
| `1` | `Potato___Late_blight` | Potato | Late Blight (*Phytophthora infestans*) | High |
| `2` | `Potato___healthy` | Potato | Healthy / Optimal | Low |
| `3` | `Tomato___Bacterial_spot` | Tomato | Bacterial Spot (*Xanthomonas*) | High |
| `4` | `Tomato___Early_blight` | Tomato | Early Blight (*Alternaria solani*) | Medium |
| `5` | `Tomato___Late_blight` | Tomato | Late Blight (*Phytophthora infestans*) | High |
| `6` | `Tomato___Yellow_Leaf_Curl_Virus` | Tomato | TYLCV (Begomovirus / Whitefly vector) | Critical |
| `7` | `Tomato___healthy` | Tomato | Healthy / Optimal | Low |

### 2.2 Model & Input Invariants
- **Input Resolution**: $224 \times 224 \times 3$ RGB.
- **Normalization**: MobileNetV2 standard: $\frac{x}{127.5} - 1.0 \in [-1.0, 1.0]$.
- **Base Architecture**: MobileNetV2 pretrained on ImageNet (alpha = 1.0).
- **Classification Head**: `GlobalAveragePooling2D` $\to$ `Dropout(0.3)` $\to$ `Dense(8, activation='softmax')`.
- **Training Strategy**: Two-phase transfer learning:
  - **Phase 1**: Frozen backbone, learning rate $1\times 10^{-3}$, Adam optimizer, categorical crossentropy with inverse-frequency class weights.
  - **Phase 2**: Top 30 backbone layers unfrozen, learning rate $1\times 10^{-5}$, Adam optimizer, fine-tuning.
- **Random Seed**: Fixed at `42` across NumPy, Python, TensorFlow, and dataset split generators.

---

## 3. Directory Blueprint & Module Roles

```
c:\F\FarmGuard-X\
├── .gitignore                          # Clean ignore rules: preserves portable split_manifest.csv
├── README.md                           # Project readme & Quickstart
├── index.html                          # Offline-ready PWA Web App interface
├── app.js                              # Client UI logic, camera access, offline state management
├── styles.css                          # Modern responsive CSS design system
├── manifest.json & sw.js               # Progressive Web App manifest & Service Worker
│
├── backend/                            # FastAPI Backend (Python 3.11)
│   ├── app/
│   │   ├── main.py                     # App entry point, CORS, static uploads mount, router registration
│   │   ├── core/
│   │   │   ├── config.py               # Pydantic v2 settings (JWT secrets, DB url, upload paths)
│   │   │   └── security.py             # bcrypt password hashing & PyJWT token generator
│   │   ├── db/
│   │   │   ├── database.py             # SQLAlchemy engine & SessionLocal dependency
│   │   │   └── models.py               # ORM tables: User, Prediction
│   │   ├── schemas/
│   │   │   ├── auth.py                 # Pydantic schemas: UserCreate, UserResponse, Token
│   │   │   ├── prediction.py           # PredictionRequest, PredictionResponse, Recommendation schemas
│   │   │   └── dashboard.py            # Summary metrics and disease breakdown schemas
│   │   ├── services/
│   │   │   ├── auth_service.py         # Registration, credential authentication, user queries
│   │   │   ├── prediction_service.py   # Image upload handling, inference orchestration, DB logging
│   │   │   ├── recommendation_service.py# Lookup for dual-action treatment plans from JSON
│   │   │   ├── history_service.py      # Historical diagnostic retrieval per farmer
│   │   │   └── dashboard_service.py    # Aggregate stats, severity alerts, scan counts
│   │   ├── api/
│   │   │   ├── deps.py                 # FastAPI dependency: get_current_user (Bearer JWT)
│   │   │   └── routes/
│   │   │       ├── auth.py             # POST /register, POST /login, GET /me
│   │   │       ├── predict.py          # POST /predict (multipart file upload)
│   │   │       ├── history.py          # GET /history, GET /history/{id}
│   │   │       └── dashboard.py        # GET /dashboard/stats
│   │   ├── ai/
│   │   │   ├── preprocess.py           # OpenCV 224x224 RGB conversion and normalization
│   │   │   ├── model_loader.py         # PyTorch/TFLite/Keras model loader with fallback mock
│   │   │   └── predictor.py            # End-to-end inference handler with confidence scores
│   │   └── data/
│   │       └── recommendations.json    # Verified agronomic advisory database (organic & chemical)
│   ├── tests/
│   │   ├── conftest.py                 # In-memory SQLite fixtures
│   │   ├── run_tests.py                # Standalone test runner for backend test suite
│   │   ├── test_auth.py                # JWT auth & user lifecycle tests
│   │   ├── test_predict.py             # Multi-part upload and inference endpoint tests
│   │   ├── test_dashboard.py           # Metrics aggregation tests
│   │   ├── test_db.py                  # Database model schema tests
│   │   └── test_recommendation.py      # Recommendation schema & disease mapping tests
│   ├── farmguard.db                    # Development SQLite database
│   └── requirements.txt                # FastAPI, SQLAlchemy, Pydantic v2, PyJWT, bcrypt, opencv-python
│
├── farmguard_ai/                       # Production ML Pipeline (TensorFlow / Keras)
│   ├── configs/
│   │   └── mobilenet_v2_int8.yaml      # Master experiment configuration (seed, splits, hparams)
│   ├── data/
│   │   ├── 01_raw/                     # Raw image downloads (PlantVillage color dataset)
│   │   ├── 02_processed/               # Provenance manifests, audit reports, corrupt image logs
│   │   ├── 03_splits/
│   │   │   └── split_manifest.csv      # 14,136-row auditable split manifest (Train/Val/Test + group IDs)
│   │   └── 04_experiments/             # Model checkpoints, TensorBoard logs, exported models
│   ├── scripts/
│   │   ├── 01_prepare_data.py          # CLI for acquisition, dedup, specimen grouping, 70/15/15 split
│   │   └── 02_train_model.py           # CLI for MobileNetV2 Phase 1 & 2 training + CPU smoke test
│   ├── src/
│   │   ├── config.py                   # YAML config loader with validation & immutable seed control
│   │   ├── data/
│   │   │   ├── acquisition.py          # Dataset download verification, class mapping, git provenance
│   │   │   ├── validator.py            # Image corruption checks, RGB validation, min dimension bounds
│   │   │   ├── deduplicator.py         # MD5 checksum and dhash near-duplicate computation
│   │   │   ├── grouper.py              # Specimen grouping engine (Hamming distance Hd <= 6 clustering)
│   │   │   ├── splitter.py             # Grouped stratified 70/15/15 dataset partitioning
│   │   │   ├── leakage_checker.py      # Mathematical zero-leakage set-intersection assertions
│   │   │   ├── auditor.py              # Generates JSON and Markdown audit reports
│   │   │   ├── loader.py               # tf.data.Dataset pipeline with prefetching & batching
│   │   │   ├── augmentation.py         # Data augmentation (flip, rotation, zoom, contrast)
│   │   │   └── provenance.py           # Cryptographic manifest generation and data licensing tracking
│   │   └── models/
│   │       ├── builder.py              # MobileNetV2 architecture builder + Phase 1 & 2 configurers
│   │       ├── class_weights.py        # Balanced & inverse frequency class weight computation
│   │       └── trainer.py              # Two-phase training loop orchestration with EarlyStopping & ModelCheckpoint
│   └── tests/                          # Comprehensive ML unit test suite (27 passing tests)
│       ├── test_config.py
│       ├── test_acquisition.py
│       ├── test_validator.py
│       ├── test_deduplicator.py
│       ├── test_grouper.py
│       ├── test_splitter.py
│       ├── test_leakage_checker.py
│       ├── test_auditor.py
│       ├── test_loader.py
│       ├── test_provenance.py
│       ├── test_builder.py
│       ├── test_class_weights.py
│       └── test_trainer.py
│
└── docs/
    ├── project-overview.md
    └── PROJECT_STATE_FOR_LLM.md        # This document
```

---

## 4. Current Milestone Status & Verified Evidence

| SDLC Phase / Sprint | Module | Status | Verified Evidence |
|:---|:---|:---:|:---|
| **Sprint 1: Backend MVP** | FastAPI App, DB, Auth, Predict, Dashboard | **COMPLETED** | `backend/tests/run_tests.py` passing 6/6 tests. JWT auth, SQLite schema, static file uploads, and treatment recommendations fully operational. |
| **Sprint 1.5: Data Pipeline** | Provenance, Dedup, Grouping, Splitting, Audit | **COMPLETED** | 14,136 images processed from PlantVillage benchmark. 14 exact duplicates identified. 644 candidate clusters (1,829 images) grouped via $H_d \le 6$ dhash. Zero-leakage assertions passed ($100\%$). Portable `split_manifest.csv` generated. |
| **Sprint 2A: Model Pipeline** | MobileNetV2 Architecture, Class Weights, Two-Phase Trainer | **COMPLETED** | Full pipeline verified with CPU synthetic forward/backward pass. Class weights calculated on train split (inverse frequency). All 27 tests in `farmguard_ai/tests` passing. |
| **Sprint 2B: Full GPU Training** | Real Training Run & Metric Evaluation | **PENDING** | Ready to run: `python farmguard_ai/scripts/02_train_model.py --gpu_run`. |
| **Sprint 3: Quantization & Edge** | TFLite INT8 Quantization & Calibration | **PENDING** | Configured in YAML (`target_max_f1_drop: 0.01`, 200 calibration samples). Needs trained weights. |
| **Sprint 4: Integration** | Connect PWA Frontend to Backend API & TFLite | **PENDING** | PWA UI exists in root (`index.html`); needs wiring to FastAPI `/api/v1/predict` and offline service worker cache. |

### Test Verification Summary:
- **Backend Test Suite**: 6 tests passed in `~1.9s`.
- **ML Pipeline Test Suite**: 27 tests passed in `~43.6s` (including full model compilation, Phase 1 & Phase 2 weight updates, and checkpoint saving).
- **Total Tests**: **33 / 33 passing (100% success rate)**.

---

## 5. Dataset & Splitting Facts (Audited)

- **Source Dataset**: PlantVillage Benchmark Dataset (Color Subset).
- **License**: CC BY 4.0.
- **Total Valid Images**: 14,136.
- **Specimen Groups**: 12,937 unique groups.
- **Split Distribution**:
  - **Train (70%)**: 9,905 images across 9,055 specimen groups.
  - **Validation (15%)**: 2,095 images across 1,940 specimen groups.
  - **Test (15%)**: 2,136 images across 1,942 specimen groups.
- **Zero Leakage Check**:
  $$\text{Train\_Groups} \cap \text{Val\_Groups} = \emptyset \quad (\text{PASSED})$$
  $$\text{Train\_Groups} \cap \text{Test\_Groups} = \emptyset \quad (\text{PASSED})$$
  $$\text{Val\_Groups} \cap \text{Test\_Groups} = \emptyset \quad (\text{PASSED})$$
  $$\text{Train\_MD5} \cap \text{Test\_MD5} = \emptyset \quad (\text{PASSED})$$

---

## 6. How to Run, Test, and Reproduce

### 6.1 Environment Preparation
Python 3.11 on Windows. Always set `PYTHONPATH` to include the repository root:
```powershell
$env:PYTHONPATH = "c:\F\FarmGuard-X"
```

### 6.2 Running All Test Suites
```powershell
# 1. Run Backend Unit & Integration Tests (6 tests)
cd c:\F\FarmGuard-X
python backend/tests/run_tests.py

# 2. Run AI / ML Pipeline Unit Tests (27 tests)
$env:PYTHONPATH = "c:\F\FarmGuard-X"
python -m unittest discover -s farmguard_ai/tests -p "test_*.py"
```

### 6.3 Executing the AI Scripts
```powershell
# Data Preparation, Dedup, Grouping & Zero-Leakage Audit:
python farmguard_ai/scripts/01_prepare_data.py --config farmguard_ai/configs/mobilenet_v2_int8.yaml

# MobileNetV2 Architecture & CPU Smoke Test (1-epoch synthetic verification):
python farmguard_ai/scripts/02_train_model.py --config farmguard_ai/configs/mobilenet_v2_int8.yaml --smoke_test

# Full GPU Training (When GPU or training host is ready):
python farmguard_ai/scripts/02_train_model.py --config farmguard_ai/configs/mobilenet_v2_int8.yaml --gpu_run
```

### 6.4 Running the FastAPI Backend
```powershell
cd c:\F\FarmGuard-X\backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# Interactive Swagger Documentation: http://localhost:8000/docs
```

---

## 7. Git & Version Control Status

In `c:\F\FarmGuard-X` on branch `main`:
- **Staged for Commit**: All modular `farmguard_ai` files, scripts, unit tests, configurations, and `split_manifest.csv`.
- **Recommended Next Git Command**:
  ```bash
  git commit -m "feat(ml): sprint 1.5 data pipeline & sprint 2a mobilenetv2 training architecture"
  git push origin main
  ```

---

## 8. Master Copy-Paste Prompt for Other LLMs

> **Instructions for the User**: Copy and paste the block below into any other LLM chat session (Claude 3.7, ChatGPT GPT-4o, Gemini 1.5 Pro, DeepSeek, etc.) to immediately bring that LLM up to full speed without needing to re-explain anything.

```markdown
You are a Senior Principal Machine Learning Engineer and Full-Stack Architect working on the "FarmGuard X" project.

### Project Context & Baseline:
- Project: FarmGuard X (AI Crop Pathology & Advisory Platform for Indian farmers).
- Repository: c:\F\FarmGuard-X (Git branch: main).
- Stack: Python 3.11, TensorFlow/Keras (MobileNetV2), FastAPI, SQLite + SQLAlchemy, Pydantic v2, PyJWT, Vanilla JS/PWA frontend.

### What is Already Built & Verified (33/33 Tests Passing):
1. Backend MVP (Sprint 1): Complete FastAPI app with JWT authentication (/api/v1/login, /register, /me), disease prediction endpoint (/api/v1/predict), prediction history (/api/v1/history), analytics dashboard (/api/v1/dashboard), and dual organic/chemical treatment recommendation engine.
2. Data Pipeline (Sprint 1.5): PlantVillage color dataset (14,136 images, 8 classes) audited. Near-duplicate clustering with dhash (Hamming distance <= 6) and MD5 deduplication. Grouped stratified 70/15/15 split generated into `farmguard_ai/data/03_splits/split_manifest.csv` with mathematically verified zero data leakage.
3. Model Architecture & Trainer (Sprint 2A): MobileNetV2 with two-phase transfer learning (Phase 1 frozen backbone, Phase 2 top 30 layers unfrozen). Inverse-frequency class weights computed from training split to tackle 35:1 class imbalance. CPU smoke test verified.
4. Test Suites: 6 backend tests in `backend/tests/run_tests.py` and 27 AI tests in `farmguard_ai/tests` all passing.

### Invariants to Maintain:
- Exactly 8 classes in strict order:
  0: Potato___Early_blight, 1: Potato___Late_blight, 2: Potato___healthy,
  3: Tomato___Bacterial_spot, 4: Tomato___Early_blight, 5: Tomato___Late_blight,
  6: Tomato___Yellow_Leaf_Curl_Virus, 7: Tomato___healthy.
- Input image size: 224x224x3, MobileNetV2 normalization [-1.0, 1.0].
- Seed: 42.
- PYTHONPATH: Always points to repo root (`c:\F\FarmGuard-X`).

### Immediate Next Tasks:
1. Sprint 2B: Run and evaluate the full GPU training pipeline (`02_train_model.py --gpu_run`), compute confusion matrix, per-class precision/recall/F1, and loss curves.
2. Sprint 3: Implement Post-Training INT8 Quantization (TFLite Converter) targeting < 15MB model size and < 1% F1 loss drop using representative dataset from train split.
3. Sprint 4: Wire backend `app/ai/model_loader.py` to load the trained model weights and connect frontend PWA to FastAPI endpoints.

Please confirm you understand this project state and tell me what step we should tackle first.
```
