# FarmGuard X — UI Design Contract (`UI-SPEC.md`)
**Document Designation:** Enterprise Frontend Architecture & De-AI Sanitization Contract  
**Phase Reference:** Phase 3D/3F Frontend & Client Experience  
**Status:** Approved Prototype Specification  
**Design Lead:** FarmGuard X Agronomy UX Engineering  

---

## 1. Executive Summary & Design Transformation

### 1.1 The Anti-AI Problem Statement
Most modern prototypes built by artificial intelligence tools suffer from unmistakable aesthetic and structural clichés:
- Neon purple (`#8b5cf6`) and cyan glowing drop-shadows that scream *"generic chatbot template"*.
- Artificial buzzwords plastered on every button: *"AI 4.2"*, *"Run AI Neural Scan"*, *"AI Primary Prediction"*.
- Messy inline styles scattered across HTML instead of disciplined CSS architecture.
- Gimmicky visual artifacts that look like an undergraduate computer science toy rather than a **clinical agricultural diagnostic instrument**.

### 1.2 The Transformation Directives
1. **Color Scheme Overhaul**: Replace all neon glows with an authentic **Soil & Foliar Bio-Industrial Palette**:
   - Base Surface: Fertile Peat Earth (`#0c1410` / `#111b16`)
   - Foliage Primary: Deep Chlorophyll Emerald (`#15803d` / `#22c55e`)
   - Pathological Status: Crimson Blight (`#b91c1c`), Ochre Chlorosis (`#d97706`), Bacterial Rust (`#c2410c`)
   - Clinical Steel: Slate Agronomy Blue (`#0284c7`)
2. **Complete Buzzword Sanitization ("De-AI")**:
   - Remove all occurrences of "AI" from operational labels. Replace with authoritative agronomic terms: *"Specimen Analysis"*, *"Pathological Assessment"*, *"Edge Diagnostics"*, *"Etiology Dossier"*.
3. **Prototypic Elegance & Code Maintainability**:
   - Eliminate cluttered inline styling dumps; consolidate into modular, well-commented CSS classes.
   - Code must read as clean, honest, prototype-grade JavaScript that any engineering evaluator can inspect, understand, and defend in 30 seconds.

---

## 2. Color Palette Specification

```
BASE EARTH LAYER
┌──────────────────────────────────────────────────────────────┐
│  --surface-ground:    #0c1410  (Deep Fertile Peat)          │
│  --surface-panel:     #121d18  (Organic Silt Bed)            │
│  --surface-elevated:  #182720  (Tactile Raised Surface)      │
│  --border-subtle:     rgba(34, 197, 94, 0.14) (Hairline)     │
│  --border-active:     rgba(34, 197, 94, 0.35) (Focus Ring)   │
└──────────────────────────────────────────────────────────────┘

DIAGNOSTIC PATHOLOGY TIERS
┌──────────────────────────────────────────────────────────────┐
│  --blight-critical:   #dc2626  (Late Blight Necrosis Alert)  │
│  --blight-warning:    #d97706  (Early Blight Alternaria Halo)│
│  --bacterial-alert:   #ea580c  (Xanthomonas Stippling)       │
│  --healthy-canopy:    #16a34a  (Vigorous Crop Tissue)        │
│  --chem-synthetic:    #0284c7  (FRAC Chemical Advisory)      │
│  --bio-organic:       #15803d  (Trichoderma Biocontrol)      │
└──────────────────────────────────────────────────────────────┘

TYPOGRAPHIC CONTRAST RATIOS (WCAG AAA)
┌──────────────────────────────────────────────────────────────┐
│  --text-main:         #f0fdf4  (Pure Mint White, 14.5:1)     │
│  --text-secondary:    #a7f3d0  (Leaf Sage, 10.8:1)           │
│  --text-subdued:      #6ee7b7  (Subdued Foliar Mint, 7.2:1)  │
│  --text-label:        #86efac  (Technical Metrics Label)     │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Component & Layout Architecture

### 3.1 Top Tactical Bar
- **Brand**: `FarmGuard X` with subtitle `Field Laboratory Console` (Replacing `AI 4.2`).
- **Telemetry Indicators**:
  - `Offline Edge Engine (On-Device)`
  - `Cluster Plot Selector` (Nashik Block 4B / Pune Plot 12)
  - `🌐 English / हिंदी` (Instant vernacular toggle)
  - `Export Certificate` (Print/PDF A4 report trigger)

### 3.2 Foliage Specimen Reticle (1:1 Aspect Ratio)
- Standardized $224 \times 224$ MobileNetV2 input viewport.
- Precision medical-grade crosshairs and dashed corner alignment reticles.
- Bounding coordinate badge showing detected pathogen lesion area (`Phytophthora infestans (97.4%)`).

### 3.3 Clinical Diagnosis Hero
- **Header**: Primary disease name with vernacular subtitle (`Tomato Late Blight / टमाटर का पछेती झुलसा रोग`).
- **Status Badge**: Solid semantic classification badge (`🚨 Critical Severity Oomycete Infection`).
- **Softmax Confidence Ring**: Clean SVG circular progress meter with tabular percentage readout (`97.4%`).
- **Etiology Grid**:
  - *Observed Symptoms* (Bullet badges)
  - *Causal Pathogen* (*Phytophthora infestans* / Oomycete)
  - *Cultural Precautions* (Drip irrigation conversion)
  - *Expected Recovery Horizon* (7–14 days)

### 3.4 Differential Triage & Rule-Out Panel
- **Top-3 Probability Distribution**:
  - Late Blight: 97.4%
  - Early Blight: 1.8%
  - Bacterial Spot: 0.8%
- **Negative Differential Justification**:
  - *"Clinical Exclusion: Alternaria solani ruled out due to lack of concentric target-board ring geometry."*

### 3.5 Knapsack Sprayer Tank Calibrator (टंकी कैलकुलेटर)
- Field Area Input (Acres / Hectares / $\text{m}^2$).
- Computes standard **15-Liter Indian Knapsack Sprayer Tanks**:
  - Total tanks needed (e.g. `10 Tanks`).
  - Active ingredient dosage per tank (`30g powder / ~2 level measuring caps`).
  - Total water volume (`150 Liters`).
  - Statutory **Pre-Harvest Interval (PHI)** countdown warning.

---

## 4. De-AI Lexicon Mapping

| AI Generated Cliché | Sanitized Agronomic Prototype Term |
| :--- | :--- |
| `AI 4.2` | `Field Lab v1.2` |
| `AI Status: Active` | `Edge Runtime: Active` |
| `Run AI Neural Scan` | `Analyze Leaf Specimen` |
| `AI Primary Prediction` | `Pathological Assessment` |
| `Initializing Offline AI Scanning Engine...` | `Ingesting foliage specimen (MobileNetV2 INT8)...` |
| `Custom image loaded. Running AI model analysis...` | `Analyzing leaf sample (224x224 RGB pathology extractor)...` |
| `AI Diagnosis` (Sidebar nav) | `Pathology Diagnosis` |

---

## 5. Prototype Code Quality Verification
The codebase is structured to be clean, transparent, and completely defendable:
- Zero obfuscated dependencies.
- Vanilla JavaScript with modern ES6+ event handling and clean DOM updates.
- Native HTML5 Canvas pixel sampling conforming directly to MobileNetV2 $224 \times 224$ RGB invariants.
- Clean-room `localStorage` audit logging.
