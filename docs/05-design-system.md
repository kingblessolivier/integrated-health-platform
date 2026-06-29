# 05 — Design System

The foundation every face is built on. Multi-platform (React web, Flutter mobile,
SMS/USSD, ambulance tablet) means **shared design tokens** are mandatory so one source
of truth drives both React (CSS variables) and Flutter (Dart theme).

## Color

Color does functional work here — it carries **state**, so semantic colors are reserved
*only* for their meaning and never used decoratively.

### Brand
| Role | Hex | Use |
|---|---|---|
| Primary teal-green | `#0E7C7B` | Brand, accents, active states |
| Primary deep green | `#06402B` | Top bar, headers, dark surfaces (nods to Rwanda) |
| Primary tint | `#E6F2F1` | Backgrounds, selected fills |

### Semantic (load-bearing)
| Meaning | Hex | Use |
|---|---|---|
| 🔴 Critical / Emergency | `#D32F2F` | SOS, interaction alerts, expired batch, account lock |
| 🟠 Warning / Offline-autonomous (**fill only**) | `#F5A623` | Sync banner (offline), low stock, licence expiring — **always with dark ink `#1A1A2E` text (8.4:1); never white (white-on-amber is only 2.0:1, fails AA)** |
| 🟠 Warning (**text / icon on white**) | `#B26A00` | The amber foreground variant, darkened to meet 4.5:1 — use this whenever amber is a glyph or label colour, never the bright fill |
| 🟢 Success / Synced / Healthy | `#2E7D32` | Synced banner, claim paid, in-range vitals |
| 🔵 Info / Neutral action | `#1565C0` | Links, info notices (kept distinct from brand teal) |

### Neutrals
| Role | Hex |
|---|---|
| Ink / primary text | `#1A1A2E` |
| Secondary text | `#5A6472` |
| Border / divider | `#D9DEE4` |
| App background | `#F4F6F8` |
| Surface / card | `#FFFFFF` |

### Data-visualization (colorblind-safe, distinct from alerts)
Qualitative series use the **Okabe–Ito** palette — a set engineered to stay distinct under
deuteranopia, protanopia, and tritanopia (the earlier ad-hoc set had two greens and a
green/blue-grey luminance collision that fail under red-green CVD):

`#E69F00 · #56B4E9 · #009E73 · #0072B2 · #D55E00 · #CC79A7 · #F0E442`

- Cap a single chart at ~7 categories; beyond that, group or facet rather than add hues.
- `#F0E442` (yellow) is a **fill only** — outline it and never use it as text on white.
- **Choropleth / disease maps** use a single-hue **sequential teal ramp** (sequential ramps
  are inherently CVD-safe).
- None of the qualitative hues may be read as state — keep them clear of the red/amber/green
  semantic meanings.

**Discipline:** Teal = brand. Red/Amber/Green = state only. Blue = info. Greys =
everything else. Never use color alone — always pair with an icon + text label.

### Tokens — ramps & semantic roles
Single hex values are not enough for real UI. Define a **tonal ramp (50→900)** per brand and
semantic colour, then map **semantic role tokens** onto the ramp so one source drives React
(CSS variables) and Flutter (Dart `ColorScheme`) identically — the approach used by IBM
Carbon, SAP Fiori, and Material 3:

- Roles: `--color-bg`, `--color-surface`, `--color-text`, `--color-text-secondary`,
  `--color-border`, and per-state `*-fg` / `*-bg` (e.g. `--color-danger-fg`,
  `--color-warning-bg`), each with `hover` / `pressed` / `disabled` steps.
- The subtle divider `#D9DEE4` (only 1.25:1 on the app background) is for decorative
  separation; **interactive control outlines need a darker border token (≥ 3:1)** to meet
  WCAG 2.2 (1.4.11).

## Typography

Humanist sans (**Inter**), legible at small sizes and in sunlight.

| Token | Size | Use |
|---|---|---|
| Display | 32 | Page titles |
| H1 | 24 | Section headers |
| H2 | 20 | Sub-sections |
| Body | 16 | Default |
| Caption | 13 | Metadata, labels |

Must render **Kinyarwanda diacritics** cleanly; plan for ~30% text expansion across
Kinyarwanda / French / English.

## Spacing & density

- 8px base grid; cards 8px radius; subtle shadows.
- **Two density modes:** dense (clinical desktop, dashboards) vs spacious with ≥48dp tap
  targets (CHW, patient, ambulance).

## Core components

NIDA-lookup field · longitudinal timeline · FEFO batch picker · status badge ·
**sync banner** · barcode-scan overlay · consent toggle · KPI card · drill-down map ·
**command bar** · tile launcher.

## Accessibility & inclusion

- **WCAG 2.2 AA**: body text ≥ 4.5:1, large text / UI ≥ 3:1.
- High contrast for **sunlight readability** (CHWs, ambulance crews work outdoors).
- Icons **always paired with text labels** (low-literacy users).
- Status **never by color alone**.
- Screen-reader support; large tap targets.
- Test every semantic color in grayscale + a deuteranopia simulator before shipping.

## Per-face tone

- **Patient app:** warmer, friendlier, more whitespace, multilingual.
- **Clinical / dashboards:** neutral, dense; saturated color reserved for status.
- **Ambulance tablet:** consider a dark surface so a bright screen doesn't blind a night
  driver; high-contrast vitals.
