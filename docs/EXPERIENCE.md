---
status: final
version: "1.0.0"
product: "FarmGuard X"
design_reference: "docs/DESIGN.md"
target_users:
  - name: "Ramesh Patel"
    role: "Smallholder Solanaceae Farmer (Nashik, Maharashtra)"
    device: "Budget 4G Android Phone (MediaTek Helio P22), cracked screen, sunlight glare"
    context: "Standing in Field Plot 4B, zero internet bars, observing water-soaked brown foliar rot"
  - name: "Dr. Sunita Sharma"
    role: "Block Agricultural Extension Officer (KVK / ICAR)"
    device: "Ruggedized 10-inch Android Tablet / Field Laptop"
    context: "Reviewing 15 village cluster inspections, auditing chemical spray resistance and advising biological rotation"
---

# FarmGuard X — Experience & Behavioral Specification (`EXPERIENCE.md`)
**System Designation:** Field-Hardened Agricultural Intelligence & Diagnostic Experience  
**Core Behavioral Invariant:** *Zero-Latency Offline Autonomy with Clinical Agronomic Precision*

---

## 1. Foundation & Platform Architecture

FarmGuard X is architected as an **Offline-First Progressive Web Application (PWA)** optimized for extreme field resilience:
- **Primary Form Factor**: Mobile-first portrait viewport ($360\text{px} \times 800\text{px}$ baseline) with fluid responsiveness scaling to desktop agronomist consoles ($1440\text{px}$).
- **Visual Design Reference**: Inherits 100% of tokens, colors, elevation, and typography from [`docs/DESIGN.md`](file:///c:/F/FarmGuard-X/docs/DESIGN.md).
- **Execution Invariant**: Every primary user flow—image ingestion, MobileNetV2 preprocessing, neural inference, differential diagnosis, dosage calculation, and report generation—must execute **100% client-side** without network dependency.

---

## 2. Information Architecture (IA)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TOP TACTICAL APP BAR                            │
│  [Logo: FarmGuard X]   [Field 4B - Tomato Plot]   [Hindi / Eng Toggle] │
│  [Hardware Engine: INT8 WASM SIMD · 42ms]   [Offline Sync: 0 Pending]  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
    ┌───────────────────────────────┴───────────────────────────────┐
    │                                                               │
┌───▼───────────────────────────┐       ┌───────────────────────────▼───┐
│     MODULE A: FIELD LENS      │       │    MODULE B: CLINICAL TRIAGE  │
│                               │       │                               │
│ • Precision Reticle (1:1 224) │       │ • Hero Diagnosis & Hindi Name │
│ • 8 Scoped Solanaceae Presets │──────>│ • Softmax Probability Gauge   │
│ • Real Leaf Drag / Camera In  │       │ • Differential Breakdown (Top3│
│ • Ambient Microclimate Risk   │       │ • Pathogen & Etiology Dossier │
│   (RH 92%, 18°C -> Blight 88%)│       │ • Verified Symptom Checklist  │
└───┬───────────────────────────┘       └───┬───────────────────────────┘
    │                                       │
    └───────────────────────┬───────────────┘
                            │
┌───────────────────────────▼───────────────────────────────────────────┐
│              MODULE C: INTEGRATED TREATMENT & PRESCRIPTION            │
│                                                                       │
│ • Tier 1: Biological / Organic (*Trichoderma viride*, Neem Azadiracht)│
│ • Tier 2: Chemical Fungicide Schedule (FRAC 4 Metalaxyl + FRAC M03)   │
│ • Tier 3: Cultural Sanitation & Pruning Protocol                      │
└───────────────────────────────────┬───────────────────────────────────┘
                                    │
┌───────────────────────────────────▼───────────────────────────────────┐
│             MODULE D: KNAPSACK SPRAYER CALIBRATOR & LOG               │
│                                                                       │
│ • Field Area Input (Acres / Hectares / Guntha)                        │
│ • 15L Knapsack Sprayer Tank Count Calculator (टंकी)                   │
│ • Grams/Milliliters per Tank & Measuring Scoop Equivalence            │
│ • Pre-Harvest Interval (PHI) Countdown & Water Runoff Safety          │
│ • LocalStorage Inspection Archive & Print Agronomy Certificate        │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 3. Voice, Tone & Microcopy

FarmGuard X speaks with the authoritative, supportive voice of a **Senior Research Agronomist standing beside the farmer in the field**:
- **Bilingual Clarity**: High-priority findings are presented bilingually (e.g., *"पत्ती झुलसा रोग (Tomato Late Blight)"*).
- **No Ambiguous Jargon**: Do not tell a farmer to *"Apply 0.05% active ingredient solution"*. State: *"Mix 30 grams (2 standard measuring caps) of Metalaxyl-Mancozeb powder per 15-Liter knapsack sprayer tank."*
- **Actionable & Preventative**: Always explain *why* an intervention is necessary and how to prevent pathogen re-inoculation (e.g., pruning bottom 30cm of foliage to stop rain-splash spore transfer).

---

## 4. Key Behavioral Patterns

### 4.1 Component Pattern: The Knapsack Sprayer Calibrator (टंकी कैलकुलेटर)
Undergraduate prototypes show abstract math like "1.5 kg per hectare". Real Indian smallholders spray using **15-Liter or 16-Liter backpack knapsack sprayers**.
1. Farmer inputs field size: `2.0 Acres`.
2. System computes:
   - **Tanks Required**: `8 Knapsack Tanks (15L each)` (Total 120L spray volume).
   - **Product per Tank**: `30 grams` of wettable powder.
   - **Visual Scoop Guide**: `1.5 level scoops per 15L tank`.
   - **Statutory Withholding Period**: `10 Days Pre-Harvest Interval`.

### 4.2 Component Pattern: Differential Diagnosis Breakdown
To prove genuine clinical intelligence and eliminate "black box AI" skepticism:
- Below the primary diagnosis, display the **Top-3 Class Probability Distribution**:
  - `Phytophthora infestans` (Late Blight): **97.4%**
  - `Alternaria solani` (Early Blight): **1.8%**
  - `Xanthomonas perforans` (Bacterial Spot): **0.8%**
- Display an explicit **Negative Differential Rule-Out**:
  - *"Ruled out Early Blight: Absence of concentric target-board rings on upper foliage."*
  - *"Ruled out Bacterial Spot: Lesions lack water-soaked halo stippling."*

### 4.3 Component Pattern: Microclimatic Disease Risk Index
Pathogens do not appear randomly; they explode under specific atmospheric conditions:
- Sensor Telemetry: Ambient Relative Humidity ($92\%$), Temperature ($18.5^\circ\text{C}$), Leaf Wetness Duration ($6.2\text{ hours}$).
- **Calculated Inoculation Risk Index: 88/100 (CRITICAL RISK)**.
- Explains to evaluators why the diagnostic advice is contextually synchronized with real epidemiology.

---

## 5. Interaction Primitives & Field Ergonomics

1. **One-Handed Thumb Zone**: All critical buttons (Scan, Switch Treatment Tab, Recalculate Dosage, Save Log) reside in the bottom 60% of the viewport.
2. **Muddy Fingers & Glove Compatibility**: Minimum touch target size is $48\text{px} \times 48\text{px}$ with a minimum $8\text{px}$ safety gutter.
3. **High-Contrast Sunlight Mode Toggle**: Instant toggle between Deep Peat Soil (Field Dark) and High-Luminance Contrast Mode ($16:1$ ratio) for direct outdoor sunlight viewing.
4. **Haptic & Visual Feedback**: Diagnostic completion triggers a subtle double haptic vibration (`navigator.vibrate([40, 60, 40])`) and high-visibility status banner.

---

## 6. Detailed User Journeys

### Journey 1: Ramesh Patel in Field Plot 4B (Offline Field Triage)
- **Protagonist**: Ramesh, 46-year-old tomato cultivator in Nashik.
- **Setting**: Midday, overcast, humid, standing between rows in Field Block 4B. Phone displays zero cellular signal bars.
1. **Intake**: Ramesh notices dark water-soaked blotches on his tomato leaves and rotting stems. He pulls out his phone and launches FarmGuard X from his home screen.
2. **Immediate Offline Confirmation**: The top bar indicates `📶 Offline Mode Active · 0 Pending Syncs`.
3. **Capture & Preprocessing**: Ramesh taps the camera shutter. The app ingests the leaf photo, rescales it to $224 \times 224$, and normalizes pixel values to $[-1.0, 1.0]$.
4. **Sub-100ms Inference**: The on-device MobileNetV2 WASM engine runs local inference in $42\text{ms}$.
5. **The Climax Beat (Accurate Diagnosis & Relief)**:
   - The screen renders: **"🚨 टमाटर का पछेती झुलसा रोग (Tomato Late Blight) — 97.4% Confidence"**.
   - Ramesh sees that it is *not* a viral disease (which would require burning the entire crop), but an aggressive oomycete that can be salvaged.
6. **Actionable Regimen**:
   - The app gives him an immediate 3-step action plan:
     1. Prune lower 30cm leaves immediately to halt ground-splash spores.
     2. Spray Bordeaux mixture (1%) or Metalaxyl 8% + Mancozeb 64% WP.
   - Ramesh taps the Knapsack Calibrator: enters `2.5 Acres`. The app tells him: *"Spray 10 knapsack tanks. Put 30g (2 scoops) in each 15L tank."*
7. **Offline Archival**: Ramesh taps **"Save Inspection"**. The scan is recorded into his persistent history log with GPS/Plot coordinates for future agronomist review.

---

### Journey 2: Dr. Sunita Sharma (Cluster Outbreak Audit & Resistance Management)
- **Protagonist**: Dr. Sunita, Agricultural Extension Specialist at Krishi Vigyan Kendra (KVK).
- **Setting**: Agronomist workstation reviewing farmer inspection logs across 12 village clusters.
1. **Accessing the Console**: Dr. Sunita opens FarmGuard X on her field tablet.
2. **Audit Inspection Log**: She reviews Ramesh's inspection record from Plot 4B.
3. **Clinical Validation**:
   - She inspects the **Differential Diagnosis** breakdown: confirms that Alternaria Early Blight was correctly ruled out due to lack of concentric ring geometry.
   - She verifies the **FRAC Fungicide Resistance Strategy**: notes that the farmer sprayed Copper Oxychloride 3 days prior, so the recommendation to alternate with systemic Metalaxyl (FRAC 4) correctly prevents single-site fungal resistance buildup.
4. **Official Prescription Export**: Dr. Sunita clicks **"Export Report"**, generating a formatted, stamped A4 Clinical Agronomy Certificate for the village cooperative credit society.

---

## 7. Accessibility Floor

- **Color Invariance**: No critical diagnostic state is communicated by color alone. Every badge pairs color with an explicit semantic icon and text label (e.g., `🚨 CRITICAL BLIGHT`, `⚠️ MODERATE WARNING`, `✅ HEALTHY CANOPY`).
- **Screen Reader Protocol**: All dynamic counters (confidence gauge, knapsack tank calculations) use `aria-live="polite"` regions so assistive software announces results without disorienting the user.
- **Minimum Font Scale**: Body text never renders smaller than $14\text{px}$ ($0.875\text{rem}$), ensuring readability through scratched protective screen covers.
