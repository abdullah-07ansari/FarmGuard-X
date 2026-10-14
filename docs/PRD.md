# FarmGuard X — Product Requirements Document (PRD)

**Document Version**: 1.0.0  
**Status**: APPROVED BASELINE  
**Product**: FarmGuard X (AI Crop Pathology & Agronomic Advisory Platform)  
**Author / PM**: Product Management & Machine Learning Systems Team  
**Date**: October 2026  

---

## 1. Executive Summary & Vision

### 1.1 Vision Statement
To democratize digital plant pathology and agronomic advisory for smallholder farmers across India, reducing crop loss due to preventable blights and pests by providing instant, highly accurate, offline-capable leaf diagnostics paired with dual-track recovery protocols (Organic and Chemical).

### 1.2 Problem Statement
* **Agricultural Yield Destruction**: Indian farmers lose $20\text{–}35\%$ of annual Solanaceae yields (Tomatoes and Potatoes) to late blight, early blight, bacterial spots, and yellow leaf curl virus.
* **Advisory & Diagnostic Desert**: Professional agricultural extension officers are scarce; farmers often travel kilometers or rely on unverified chemical vendor advice, resulting in pesticide overuse, soil degradation, and delayed treatment.
* **Connectivity Barriers**: Remote rural fields frequently experience 2G, intermittent, or completely severed cellular data connectivity. Cloud-only AI vision models fail in the field.

### 1.3 Value Proposition
FarmGuard X bridges the diagnostic gap by offering:
1. **Under-Second Field Diagnosis**: Instant pathological analysis from a standard smartphone camera photograph.
2. **Offline-First Resilience**: An edge-quantized MobileNetV2 neural model ($< 15\text{ MB}$) that operates on the device without requiring active network connectivity.
3. **Dual-Track Agronomic Recovery Plans**: Immediately actionable treatment plans specifying both low-cost organic remedies (neem oil, compost tea, copper soaps) and targeted chemical interventions (mancozeb, chlorothalonil) with label precautions and recovery timelines.
4. **Historical Crop Logging**: Tracking infection trends per field over time to detect recurring pathogen vectors.

---

## 2. Target Personas & User Journeys

### 2.1 Personas

#### Persona 1: Ramesh Patel — Smallholder Farmer
* **Demographics**: 42 years old, Nashik district, Maharashtra. Cultivates 3 acres of tomatoes and potatoes.
* **Tech Literacy**: Uses WhatsApp and YouTube on an entry-level Android smartphone (2 GB RAM, Android 11).
* **Pain Point**: Discovered dark, water-soaked brown lesions on lower tomato leaves following continuous monsoon drizzle. Needs immediate advice on whether it is early blight or late blight before spraying expensive chemicals.
* **Constraint**: Mobile cellular connectivity in his farm plot is zero to one bar (EDGE/intermittent).

#### Persona 2: Sunita Sharma — Village Agricultural Extension Volunteer (KVK Volunteer)
* **Demographics**: 28 years old, agricultural diploma holder assisting 50+ village households.
* **Tech Literacy**: Moderate-to-high, uses tablet and mobile apps for farmer assistance.
* **Pain Point**: Needs an objective, traceable diagnostic history tool to monitor community-wide outbreaks and demonstrate organic IPM (Integrated Pest Management) practices.

---

### 2.2 User Journeys

#### Journey 1: Offline Field Leaf Diagnosis (Ramesh)
1. **Discovery**: Ramesh spots yellowing foliage with dark concentric rings on potato leaves.
2. **Access**: Opens FarmGuard X PWA directly from his phone's home screen. The app loads instantly via Service Worker cache with an "🟢 Offline Ready" badge.
3. **Image Capture**: Points camera at an affected leaf; the app guides him with an on-screen framing reticle.
4. **Instant Inference**: Hits "Analyze Leaf". The edge neural model runs locally in $< 100\text{ ms}$, classifying the symptom as `Potato___Early_blight` with $96.4\%$ confidence.
5. **Dual Treatment Guidance**: Ramesh reviews the advisory card:
   * *Organic*: Copper soap spray every 7 days; remove lower soil-touching leaves.
   * *Chemical*: Azoxystrobin/Difenoconazole dosage per liter.
6. **Local Record**: The scan is saved to his offline inspection log. When he returns home to Wi-Fi/cellular range, the scan metadata seamlessly syncs to his cloud history.

#### Journey 2: Extension Analytics & Field Tracking (Sunita)
1. **Login**: Sunita logs into the FarmGuard X dashboard via her tablet using secure JWT credentials.
2. **Dashboard Overview**: Views summary metrics showing 154 total community scans with a surge in `Tomato___Late_blight` alerts ($38.8\%$ of active scans).
3. **Preventive Action**: Advises the village cooperative to preemptively cease overhead irrigation and apply preventive copper hydroxide barriers.

---

## 3. Product Scope & Classification Boundary

### 3.1 Supported Crops & Pathological Classes
The scope of FarmGuard X is strictly bound to 8 Solanaceae pathology classes:
1. `Potato___Early_blight` (*Alternaria solani*) — Severity: Medium
2. `Potato___Late_blight` (*Phytophthora infestans*) — Severity: High
3. `Potato___healthy` — Severity: Low / Optimal
4. `Tomato___Bacterial_spot` (*Xanthomonas spp.*) — Severity: High
5. `Tomato___Early_blight` (*Alternaria solani*) — Severity: Medium
6. `Tomato___Late_blight` (*Phytophthora infestans*) — Severity: High
7. `Tomato___Yellow_Leaf_Curl_Virus` (*TYLCV*) — Severity: Critical
8. `Tomato___healthy` — Severity: Low / Optimal

---

## 4. Functional Requirements (FR)

### Module 1: Image Acquisition & Preprocessing
* **FR-1.1**: The client shall capture images directly through the device camera API or allow file uploads from gallery storage (JPEG, PNG).
* **FR-1.2**: The application shall validate image integrity before submission and reject corrupt, unreadable, or non-image files with clear user feedback.
* **FR-1.3**: The preprocessing pipeline shall standardize images to $224 \times 224 \times 3$ RGB format normalized to $[-1.0, 1.0]$.

### Module 2: AI Diagnostic Engine
* **FR-2.1**: The AI engine shall classify images into one of the 8 approved classes, outputting the predicted label, confidence score ($[0.0, 1.0]$), and inference latency.
* **FR-2.2**: The system shall enforce a minimum confidence threshold ($\tau = 0.65$); diagnoses below $\tau$ shall be flagged with an "Ambiguous Image / Rescan Recommended" status.
* **FR-2.3**: The system shall support dual-tier execution: edge inference via INT8 TFLite on the client and server-side fallback inference via FastAPI.

### Module 3: Dual-Track Agronomic Advisory
* **FR-3.1**: For every diagnosed pathology, the system shall provide both **Organic/Cultural** and **Chemical/Targeted** recommendations.
* **FR-3.2**: Each recommendation shall state: Pathogen Cause, Severity Tier, Organic Treatment, Chemical Active Ingredients & Dosage, Preventive Measures, and Expected Recovery Timeline.
* **FR-3.3**: For healthy classifications, the system shall display maintenance, nutrient balance, and scouting tips.

### Module 4: Authentication & User Management
* **FR-4.1**: Farmers shall be able to register using email, full name, and password.
* **FR-4.2**: The system shall authenticate users via bcrypt password verification and issue cryptographically signed JWT Bearer tokens (60-minute expiry).
* **FR-4.3**: Guests shall be permitted to perform single-shot diagnoses without mandatory account creation.

### Module 5: Field Logging & Analytics Dashboard
* **FR-5.1**: Every authenticated diagnostic scan shall be persisted with image path, crop, disease, confidence, and timestamp.
* **FR-5.2**: Users shall be able to review their chronological scan history with pagination (`limit`, `skip`).
* **FR-5.3**: The dashboard shall aggregate aggregate metrics: total scans, healthy vs diseased ratio, active critical alerts, and disease breakdown percentages.

---

## 5. Non-Functional Requirements (NFR)

### 5.1 Performance & Latency
* **NFR-1 (Inference Latency)**: Edge inference on mobile CPU/NPU must complete in $\le 150\text{ ms}$. Cloud inference latency must not exceed $500\text{ ms}$ under standard 4G connectivity.
* **NFR-2 (Model Footprint)**: The edge INT8 TFLite model binary must not exceed $15\text{ MB}$ to ensure rapid download and minimal memory usage on low-end hardware.
* **NFR-3 (Throughput)**: The FastAPI backend must support at least 50 concurrent prediction requests with $< 1\text{ s}$ p95 response time.

### 5.2 Reliability & Availability
* **NFR-4 (Zero-Leakage Model Integrity)**: The ML training pipeline must guarantee mathematical zero data leakage ($\text{Train} \cap \text{Val} = \emptyset$) across specimen clusters grouped at $H_d \le 6$.
* **NFR-5 (Offline Durability)**: PWA core assets (HTML, CSS, JS, icon assets) must be cached via Service Worker, allowing app launch and cached advisory retrieval in full airplane mode.

### 5.3 Usability & Localization
* **NFR-6 (Visual Hierarchy)**: All disease severity indicators must use standardized color coding (Green: Healthy, Amber: Medium, Red: High/Critical).
* **NFR-7 (Simplicity)**: The primary diagnostic workflow must require no more than two clicks from app launch to diagnosis.

---

## 6. Success Metrics & Key Performance Indicators (KPIs)

| Metric | Target | Measurement Method |
|---|:---:|---|
| **Macro F1-Score (Test Set)** | $\ge 92.0\%$ | Evaluated against 2,136 held-out test images |
| **Quantization Degradation** | $< 1.0\%$ F1 loss | Macro F1 comparison: FP32 Baseline vs INT8 TFLite |
| **Offline Diagnostic Availability** | $100\%$ | Tested via Service Worker cache in airplane mode |
| **P95 Client Latency** | $< 200\text{ ms}$ | Measured on entry-level Android devices |
| **User Diagnostic Satisfaction** | $\ge 85\%$ | Post-treatment user recovery feedback rating |

---

## 7. Out of Scope (Non-Goals for Phase 3)
* Autonomous pesticide drone spraying integration.
* Commercial pesticide e-commerce checkout or payment gateway integration.
* Non-Solanaceae crops (e.g., Rice, Wheat, Cotton) — planned for Phase 4.
* Soil satellite moisture GIS telemetry.
