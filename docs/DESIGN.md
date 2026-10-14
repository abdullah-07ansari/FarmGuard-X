---
status: final
version: "1.0.0"
product: "FarmGuard X"
platform: "Mobile-First Responsive PWA & Agronomist Field Terminal"
theme: "Enterprise Agri-Intelligence / Sunlight-Hardened Bio-Industrial"
tokens:
  colors:
    brand:
      primary: "#059669"       # Deep Agricultural Emerald
      primary_dark: "#064e3b"  # Deep Canopy Green
      primary_light: "#34d399" # Young Shoot Green
      surface: "#0b1512"        # Deep Peat Soil (Field Dark)
      surface_card: "#12201b"   # Rich Organic Silt
      surface_raised: "#1a2e27" # Elevated Foliar Surface
      border_subtle: "rgba(52, 211, 153, 0.12)"
      border_strong: "rgba(52, 211, 153, 0.28)"
    pathology:
      blight_critical: "#dc2626" # Late Blight Necrosis / High Spore Alert
      blight_warning: "#f59e0b"  # Early Blight Chlorosis / Alert
      bacterial_alert: "#ea580c" # Xanthomonas Spot / Moderate Alert
      healthy_canopy: "#10b981"  # Optimal Turgid Foliage
      info_chem: "#0284c7"       # FRAC Synthetic Advisory
      bio_organic: "#16a34a"     # Trichoderma / Biocontrol
    neutral:
      text_primary: "#f0fdf4"    # Mint Off-White (14.2:1 contrast against peat)
      text_secondary: "#a7f3d0"  # Soft Leaf Sage
      text_muted: "#6ee7b7"      # Subdued Foliar Mint (WCAG AA verified)
      text_dim: "#047857"        # Background Context Labels
  typography:
    font_family_display: "'Plus Jakarta Sans', system-ui, -apple-system, sans-serif"
    font_family_mono: "'JetBrains Mono', 'Fira Code', monospace"
    font_size_xs: "0.75rem"
    font_size_sm: "0.875rem"
    font_size_base: "1.0rem"
    font_size_lg: "1.125rem"
    font_size_xl: "1.35rem"
    font_size_2xl: "1.75rem"
    font_size_display: "2.25rem"
  rounded:
    xs: "4px"
    sm: "6px"
    md: "10px"
    lg: "16px"
    pill: "9999px"
  spacing:
    xs: "4px"
    sm: "8px"
    md: "16px"
    lg: "24px"
    xl: "32px"
---

# FarmGuard X — Design Specification (`DESIGN.md`)
**System Designation:** Field-Hardened Agricultural Intelligence & Diagnostic Interface  
**Spec Standard:** Google Labs Design Specification (`design.md`)  
**Design Philosophy:** *Bio-Industrial Utility over AI Toy Novelty*

---

## 1. Brand & Style

### 1.1 Aesthetic Stance
FarmGuard X rejects the cliché "AI chatbot" aesthetic (neon purple gradients, generic floating glass cards, meaningless circular progress bars). It is engineered as a **precision agronomic instrument** designed for harsh outdoor sunlight, muddy fingertips, and high-stakes agricultural decision-making.

The visual language bridges two worlds:
1. **Soil & Canopy Organic Realism**: Earth tones rooted in rich organic peat (`#0b1512`), wet silt (`#12201b`), and chlorophyll emerald (`#059669`).
2. **Clinical Scientific Telemetry**: Crisp tabular telemetry, FRAC (Fungicide Resistance Action Committee) clinical color-coding, and micro-climatic environmental indicators.

### 1.2 Anti-Patterns Strictly Prohibited
- ❌ **No "AI Sparkles" or Magic Wands**: FarmGuard X is a diagnostic edge engine, not a generative art toy.
- ❌ **No Cluttered Skeuomorphism**: No fake leaves or cartoon tractors.
- ❌ **No Low-Contrast Faded Grays**: Field visibility under direct Indian midday sunlight ($100,000\text{ lux}$) requires strict high-contrast typography ($\ge 12:1$ contrast ratio).

---

## 2. Color Architecture & Meaning

| Role / Token | Hex Value | Agronomic & UI Context | Contrast Ratio |
| :--- | :--- | :--- | :--- |
| `surface` | `#0b1512` | Deep Peat Soil baseline surface | Baseline |
| `surface_card` | `#12201b` | Diagnostic inspection cards, telemetry panels | 1.4:1 vs base |
| `surface_raised` | `#1a2e27` | Interactive knapsack dosage calculator, active tabs | 2.1:1 vs base |
| `primary` | `#059669` | Primary action triggers, healthy leaf confirmation | 7.8:1 vs text |
| `blight_critical` | `#dc2626` | Oomycete sporulation (*P. infestans*), quarantine triggers | 6.2:1 on dark |
| `blight_warning` | `#f59e0b` | Concentric lesions (*A. solani*), moderate chlorosis | 8.9:1 on dark |
| `bacterial_alert`| `#ea580c` | Xanthomonas greasy lesions, copper bactericide alert | 7.1:1 on dark |
| `info_chem` | `#0284c7` | Synthetic chemical fungicides (FRAC 4, FRAC M03) | 6.5:1 on dark |
| `bio_organic` | `#16a34a` | Certified biological controls (*Trichoderma*, Neem Azadirachtin) | 7.2:1 on dark |
| `text_primary` | `#f0fdf4` | Clinical disease titles, dosage values, critical warnings | **14.2:1 (AAA)** |
| `text_secondary` | `#a7f3d0` | Pathogen names, application timings, symptoms | **10.8:1 (AAA)** |

---

## 3. Typography Hierarchy

```
Display / Hero Title     Plus Jakarta Sans Bold   2.25rem (36px)   Tracking -0.02em
Section Headers         Plus Jakarta Sans 700    1.35rem (22px)   Tracking -0.01em
Card Titles & Pathology  Plus Jakarta Sans 600    1.125rem (18px)  Tracking normal
Body Diagnostic Prose   Plus Jakarta Sans 400    0.95rem (15px)   Line-height 1.6
Telemetry & FRAC Codes  JetBrains Mono 600       0.82rem (13px)   Tabular figures
```

### Vernacular / Bilingual Typography
For Indian rural adoption, every diagnostic card pairs Latin scientific binomials (*Phytophthora infestans*) with clear Hindi agronomic terminology (पत्ती झुलसा रोग). Dual-script rendering utilizes system-native Noto Sans Devanagari fallbacks.

---

## 4. Layout & Spacing

### 4.1 Grid System
- **Desktop / Agronomist Console**: 12-column responsive fluid grid with fixed 260px tactical telemetry sidebar.
- **Mobile Field Viewport**: Single-column vertical stack with sticky bottom triage bar (Scan, Dose, Export).

### 4.2 Spacing Invariants
All margins, padding, and gaps derive from a strict $8\text{px}$ base grid:
- `8px` (`sm`): Badge padding, tag margins, micro-telemetry gaps.
- `16px` (`md`): Form input padding, card inner margins.
- `24px` (`lg`): Section separation, hero container padding.
- `32px` (`xl`): Primary structural module boundaries.

---

## 5. Elevation & Depth

FarmGuard X uses **tactical edge boundaries** rather than heavy blurred drop-shadows:
- **Level 0 (Base)**: Solid Peat `#0b1512`.
- **Level 1 (Card Container)**: `#12201b` with a crisp $1\text{px}$ solid border (`rgba(52, 211, 153, 0.14)`).
- **Level 2 (Active Diagnostic Focus)**: `#1a2e27` with a $2\text{px}$ left-edge pathology-state indicator (Crimson for Late Blight, Amber for Early Blight, Emerald for Healthy).
- **Level 3 (Modal / Field Log Overlay)**: `#0e1a15` with $12\text{px}$ backdrop blur and high-contrast `#34d399` hairline border.

---

## 6. Shapes & Edge Geometry

- **Data Cards**: Subtle `10px` radius (`md`). Avoids juvenile large pill radii while eliminating sharp harsh corners.
- **Tactical Buttons**: `8px` radius with $1\text{px}$ border and $44\text{px}$ minimum height to support gloved or wet hands in the field.
- **Telemetry Chips**: `pill` (`9999px`) for classification tags, FRAC resistance codes, and sync indicators.

---

## 7. Component Specifications

### 7.1 Pathology Inspection Lens (The Scanning Canvas)
- **Dimensions**: Aspect ratio locked to $1:1$ matching MobileNetV2 $224 \times 224$ input resolution.
- **Reticle**: Precision medical-grade crosshair overlay with corner brackets rather than a cartoon laser line.
- **Bounding Box**: Amber/Crimson dashed coordinate box displaying precise pixel coordinates and soft-max probability (`(x:42, y:68, w:112, h:98) · p=0.978`).

### 7.2 The Knapsack Dosage Converter
Instead of theoretical "liters per acre", the UI incorporates the **15L Rural Knapsack Tank Standard**:
- Calculates: Total Field Area $\to$ Number of 15L Knapsack Sprayer Tanks needed $\to$ Exact powder grams or liquid ml per single tank $\to$ Measuring scoop equivalent ("2 standard caps per tank").

### 7.3 Edge Telemetry Status Bar
A dedicated hardware diagnostic bar displayed directly beneath the primary header:
- **Model**: `MobileNetV2-INT8-PV8 (v1.2.0)`
- **Inference Runtime**: `WASM SIMD Edge Engine (42ms)`
- **RAM Footprint**: `14.2 MB Allocated`
- **Offline Sync Queue**: `3 Encrypted Records Buffered`
- **Environmental Hazard**: `Late Blight Risk: 88% (RH 92%, Temp 18°C)`

---

## 8. Do's and Don'ts

### Do
- ✅ **Show Differential Diagnoses**: Always display the top-3 probabilities (e.g., Late Blight 97.4%, Early Blight 1.8%, Bacterial Spot 0.8%) to prove genuine neural softmax execution.
- ✅ **Display Pre-Harvest Intervals**: Every chemical advisory must state the statutory withholding period before crop harvesting (e.g., 24 Hours for Copper Hydroxide, 14 Days for Systemic Metalaxyl).
- ✅ **Highlight Organic First**: Prioritize organic biologicals (*Trichoderma*, cold-pressed Neem) to avoid pesticide resistance buildup.

### Don't
- ❌ **Don't show out-of-scope crops**: Never show corn, apple, or grape icons. Strictly restrict to Tomato and Potato Solanaceae.
- ❌ **Don't use generic placeholder stats**: Never display unverified claims like "100% Guaranteed Cure". Pathology advice must reflect agricultural science realities.
- ❌ **Don't hide offline status**: Always indicate whether diagnosis was computed locally on edge hardware or synced via central API.
