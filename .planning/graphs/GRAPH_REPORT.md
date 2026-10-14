# Graph Report - FarmGuard-X  (2026-10-15)

## Corpus Check
- 83 files · ~90,687 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 665 nodes · 936 edges · 46 communities (41 shown, 5 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 56 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6b2a049f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- User
- 02_train_model.py
- ModelBuilder
- FarmGuard X — AI Crop Pathology Platform
- Deduplicator
- FarmGuard X — Low-Level Design (LLD) Document
- test_auth.py
- FarmGuard X — Software Requirements Specification (SRS)
- FarmGuard X — Product Requirements Document (PRD)
- 4. Top 10 Evaluator Defense Questions & Ironclad Answers
- Config
- FarmGuard X — Design Specification (`DESIGN.md`)
- .verify_records
- preprocess_image
- FarmGuard X — Comprehensive Project Progress & LLM Handoff Guide
- 01_prepare_data.py
- .verify_and_log
- DatasetSplitter
- FarmGuard X — Experience & Behavioral Specification (`EXPERIENCE.md`)
- DataValidator
- app.js
- PredictionHistoryItem
- RecommendationService
- .generate_audit_report
- Prediction
- ModelLoader
- manifest.json
- .process_and_save_prediction
- run_tests.py
- main
- DashboardService
- HistoryService
- TestModule4PredictAndHistory
- TestModule5Dashboard
- db_session
- sw.js

## God Nodes (most connected - your core abstractions)
1. `User` - 27 edges
2. `Prediction` - 18 edges
3. `RecommendationService` - 16 edges
4. `Config` - 13 edges
5. `ModelBuilder` - 12 edges
6. `get_db()` - 11 edges
7. `AuthService` - 11 edges
8. `main()` - 11 edges
9. `Deduplicator` - 11 edges
10. `DataLoader` - 11 edges

## Surprising Connections (you probably didn't know these)
- `TestAcquisition` --uses--> `Config`  [INFERRED]
  farmguard_ai/tests/test_acquisition.py → backend/app/core/config.py
- `TestConfig` --uses--> `Config`  [INFERRED]
  farmguard_ai/tests/test_config.py → backend/app/core/config.py
- `TestValidator` --uses--> `Config`  [INFERRED]
  farmguard_ai/tests/test_validator.py → backend/app/core/config.py
- `ModelTrainer` --uses--> `Config`  [INFERRED]
  farmguard_ai/src/models/trainer.py → backend/app/core/config.py
- `TrainerError` --uses--> `Config`  [INFERRED]
  farmguard_ai/src/models/trainer.py → backend/app/core/config.py

## Import Cycles
- None detected.

## Communities (46 total, 5 thin omitted)

### Community 0 - "User"
Cohesion: 0.06
Nodes (50): get_current_user(), Session, Dependency to retrieve current authenticated user using AuthService., login(), get, post, Session, Register a new user account. (+42 more)

### Community 1 - "02_train_model.py"
Cohesion: 0.07
Nodes (27): main(), Sprint 2A CLI Entrypoint: 02_train_model.py Orchestrates MobileNetV2…, AugmentationPipeline, Data Augmentation Module for FarmGuard X. Provides Keras preprocessing layers…, Builds a Keras Sequential layer for training-only data augmentation. Includes…, DataLoader, DataLoaderError, Dataset (+19 more)

### Community 2 - "ModelBuilder"
Cohesion: 0.08
Nodes (27): Config, Settings, BaseSettings, Config, Executes a lightweight 1-epoch CPU smoke test on synthetic tensors to verify…, run_smoke_test(), ModelBuilder, ModelBuilderError (+19 more)

### Community 3 - "FarmGuard X — AI Crop Pathology Platform"
Cohesion: 0.06
Nodes (28): 1.1 Guiding Principles, 1. Architectural Principles & System Goals, 2. System Context & Tier Topology, 3.1 Client Tier (Progressive Web Application), 3.2 Backend Services Tier (FastAPI Engine), 3.3 ML Engineering Subsystem (`farmguard_ai`), 3. Subsystem Architectural Breakdown, 4. Architectural Invariants (+20 more)

### Community 4 - "Deduplicator"
Cohesion: 0.10
Nodes (15): Deduplicator, Any, Path, Deduplication & Hashing Module for FarmGuard X. Computes MD5 binary hashes for…, Computes binary MD5 checksum for exact file matching., Computes Difference Hash (dhash) using PIL and numpy. Resizes to (hash_size +…, Computes Hamming distance between two hex hash strings., Enriches image records with MD5 and dhash, flags exact duplicates, and links… (+7 more)

### Community 5 - "FarmGuard X — Low-Level Design (LLD) Document"
Cohesion: 0.06
Nodes (31): 10. Traceability Matrix (Requirements to Code Modules), 1.1 Purpose, 1.2 System Scope, 1. Introduction & System Scope, 2. Component & Architecture Decomposition, 3.1 Table Definition: `users`, 3.2 Table Definition: `predictions`, 3. Detailed Database Schema & Storage Design (+23 more)

### Community 6 - "test_auth.py"
Cohesion: 0.09
Nodes (17): health_check(), get, client(), fixture, client(), create_test_image_file(), get_auth_token(), fixture (+9 more)

### Community 7 - "FarmGuard X — Software Requirements Specification (SRS)"
Cohesion: 0.07
Nodes (27): 1.1 Purpose, 1.2 Scope, 1.3 Definitions, Acronyms, and Abbreviations, 1.4 References, 1. Introduction, 2.1 Product Perspective, 2.2 Product Functions (High-Level Summary), 2.3 User Characteristics & Operating Constraints (+19 more)

### Community 8 - "FarmGuard X — Product Requirements Document (PRD)"
Cohesion: 0.07
Nodes (26): 1.1 Vision Statement, 1.2 Problem Statement, 1.3 Value Proposition, 1. Executive Summary & Vision, 2.1 Personas, 2.2 User Journeys, 2. Target Personas & User Journeys, 3.1 Supported Crops & Pathological Classes (+18 more)

### Community 9 - "4. Top 10 Evaluator Defense Questions & Ironclad Answers"
Cohesion: 0.09
Nodes (22): 1. Difference Hashing (`dhash`), 1. Executive Summary & 2-Minute Elevator Pitch, 2. 90-Second Live Demonstration Script, 2. Inverse Class Weighting, 3. Honest System Architecture & Status Matrix, 3. MobileNetV2 Normalization Invariant, 4. Top 10 Evaluator Defense Questions & Ironclad Answers, 5. Technical Mathematical Formulation Cheat Sheet (+14 more)

### Community 10 - "Config"
Cohesion: 0.13
Nodes (11): Config, ConfigError, Any, Exception, Path, Config Manager for FarmGuard X AI Pipeline. Loads YAML configurations,…, Enforce reproducible random seeds across Python environment., Factory method to parse YAML configuration file. (+3 more)

### Community 11 - "FarmGuard X — Design Specification (`DESIGN.md`)"
Cohesion: 0.10
Nodes (19): 1.1 Aesthetic Stance, 1.2 Anti-Patterns Strictly Prohibited, 1. Brand & Style, 2. Color Architecture & Meaning, 3. Typography Hierarchy, 4.1 Grid System, 4.2 Spacing Invariants, 4. Layout & Spacing (+11 more)

### Community 12 - ".verify_records"
Cohesion: 0.19
Nodes (10): DataLeakageError, LeakageChecker, Any, Exception, Path, Automated Data Leakage Verification Module for FarmGuard X. Executes…, Reads an exported split_manifest.csv and executes zero-leakage assertions., Critical exception raised when data leakage is detected between splits. (+2 more)

### Community 13 - "preprocess_image"
Cohesion: 0.15
Nodes (11): DiseasePredictor, Any, Run complete AI pipeline: 1. OpenCV preprocessing (resize 224x224, BGR->RGB,…, Core AI Predictor for crop disease classification. Processes input foliage…, preprocess_image(), Preprocess raw image (bytes or path) using OpenCV: 1. Decode/Read image into…, create_synthetic_jpeg_bytes(), Generate a synthetic green leaf image encoded as JPEG bytes. (+3 more)

### Community 14 - "FarmGuard X — Comprehensive Project Progress & LLM Handoff Guide"
Cohesion: 0.12
Nodes (17): 1. Executive Project Summary, 2.1 The 8 Target Classes (`APPROVED_LABELS`), 2.2 Model & Input Invariants, 2. Invariants & Fixed Architectural Constants, 3. Directory Blueprint & Module Roles, 4. Current Milestone Status & Verified Evidence, 5. Dataset & Splitting Facts (Audited), 6.1 Environment Preparation (+9 more)

### Community 15 - "01_prepare_data.py"
Cohesion: 0.19
Nodes (8): Sprint 1.5 CLI Entrypoint: 01_prepare_data.py Executes real dataset…, AcquisitionError, DatasetAcquisition, Exception, Real Dataset Acquisition & Provenance Verification Module for FarmGuard X.…, Exception raised during dataset acquisition or verification., Verifies that source directory contains subfolders for the 8 approved classes.…, TestAcquisition

### Community 16 - ".verify_and_log"
Cohesion: 0.18
Nodes (9): ProvenanceError, ProvenanceManager, Any, Exception, Path, Dataset Provenance & Licensing Metadata Module. Manages dataset licensing…, Exception raised for provenance or licensing failures., Verifies license compliance and records dataset provenance metadata. (+1 more)

### Community 17 - "DatasetSplitter"
Cohesion: 0.17
Nodes (10): DatasetSplitter, Any, Exception, Path, Grouped Stratified Dataset Splitter & Manifest Generator for FarmGuard X.…, Exception raised for dataset splitting errors., Splits image records at the group_id level into train, val, and test splits.…, Exports the complete auditable split_manifest.csv file. (+2 more)

### Community 18 - "FarmGuard X — Experience & Behavioral Specification (`EXPERIENCE.md`)"
Cohesion: 0.14
Nodes (13): 1. Foundation & Platform Architecture, 2. Information Architecture (IA), 3. Voice, Tone & Microcopy, 4.1 Component Pattern: The Knapsack Sprayer Calibrator (टंकी कैलकुलेटर), 4.2 Component Pattern: Differential Diagnosis Breakdown, 4.3 Component Pattern: Microclimatic Disease Risk Index, 4. Key Behavioral Patterns, 5. Interaction Primitives & Field Ergonomics (+5 more)

### Community 19 - "DataValidator"
Cohesion: 0.19
Nodes (6): DataValidator, Any, Path, Data Validation Module for FarmGuard X. Inspects raw image files, checks…, Validates all raw images in the given directory. Returns a tuple of…, TestValidator

### Community 20 - "app.js"
Cohesion: 0.35
Nodes (9): animateConfidence(), calculateDosage(), getInspections(), handleUploadedFile(), renderInspections(), runNeuralScan(), saveInspection(), showToast() (+1 more)

### Community 21 - "PredictionHistoryItem"
Cohesion: 0.29
Nodes (10): CropDistribution, DashboardResponse, DiseaseDistribution, BaseModel, Config, PredictionHistoryItem, PredictionHistoryResponse, PredictionResponse (+2 more)

### Community 22 - "RecommendationService"
Cohesion: 0.23
Nodes (6): Any, Lookup recommendations for a given disease class key. e.g.,…, RecommendationService, test_get_unknown_recommendation_fallback(), test_get_valid_recommendation(), test_recommendation_service_loading()

### Community 23 - ".generate_audit_report"
Cohesion: 0.21
Nodes (6): DatasetAuditor, Any, Path, Comprehensive Real Dataset Auditor for FarmGuard X. Compiles all dataset…, Compiles and writes full dataset audit report to JSON and Markdown., TestAuditor

### Community 24 - "Prediction"
Cohesion: 0.24
Nodes (4): Prediction, TestModule1, test_create_user_and_prediction(), Base

### Community 25 - "ModelLoader"
Cohesion: 0.25
Nodes (5): ModelLoader, Path, Model loader for MobileNetV3 / EfficientNet-B0 / YOLOv8-cls models. Loads…, Initialize classification model or fallback classifier., Return crop, disease, and recommendation key for class_id.

### Community 26 - "manifest.json"
Cohesion: 0.22
Nodes (8): background_color, description, display, icons, name, short_name, start_url, theme_color

### Community 27 - ".process_and_save_prediction"
Cohesion: 0.25
Nodes (6): PredictionService, Any, Session, UploadFile, Service handling image upload saving, AI inference, and database persistence., Process leaf image upload: 1. Validate file extension / image type. 2. Save raw…

### Community 29 - "main"
Cohesion: 0.25
Nodes (5): main(), Any, Path, Retrieves head commit hash if repository is a git clone., Records comprehensive dataset provenance and licensing metadata.

### Community 30 - "DashboardService"
Cohesion: 0.29
Nodes (5): DashboardService, Any, Session, Aggregate scan metrics for user: - Total scans - Healthy vs Diseased count &…, Service generating analytics metrics and dashboard summaries.

### Community 31 - "HistoryService"
Cohesion: 0.29
Nodes (5): HistoryService, Any, Session, Fetch paginated history items for user with recommendation details., Service retrieving user prediction scan history.

## Knowledge Gaps
- **144 isolated node(s):** `Config`, `Config`, `name`, `short_name`, `description` (+139 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `Prediction`, `TestModule5Dashboard`, `TestModule4PredictAndHistory`, `run_tests.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `main()` connect `main` to `Deduplicator`, `Config`, `.verify_records`, `01_prepare_data.py`, `DatasetSplitter`, `DataValidator`, `.generate_audit_report`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `Config` connect `Config` to `02_train_model.py`, `ModelBuilder`, `DataValidator`, `01_prepare_data.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `User` (e.g. with `AuthService` and `TestModule1`) actually correct?**
  _`User` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Prediction` (e.g. with `DashboardService` and `HistoryService`) actually correct?**
  _`Prediction` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `RecommendationService` (e.g. with `TestModule1` and `TestModule2Auth`) actually correct?**
  _`RecommendationService` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `ModelBuilder` (e.g. with `ModelTrainer` and `TrainerError`) actually correct?**
  _`ModelBuilder` has 4 INFERRED edges - model-reasoned connections that need verification._