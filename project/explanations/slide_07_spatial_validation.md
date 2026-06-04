# Slide 7 – Spatial Validation & Sensor Correlation

## What this slide shows

This slide presents the **Pearson correlation analysis** used to validate the sensor network and understand how gas concentrations relate across the mofette's measurement stack.

Two correlation matrices are displayed side-by-side:

1. **Top sensors vs. CO₂ (top_sensors_CO2_correlation.png)** — correlates the uppermost sensors in the stack with each other and with environmental variables.  
2. **Main stack vs. Side tube (CO2_main_vs_side_correlation.png)** — correlates CO₂ readings from the central monitoring column with those from a second, horizontally offset side tube.

---

## Key findings

| Observation | Value | Meaning |
|---|---|---|
| Main ↔ Side stack correlation | r > 0.85 | Gas layers are **horizontally uniform** across the chamber |
| Top sensors (18–20) correlation | r ≈ 0.5–0.7 | Weaker — exposed to ambient wind and fresh-air mixing at the boundary |
| Pressure ↔ all CO₂ sensors | negative | Barometric pressure uniformly suppresses gas levels across the entire stack |
| Temperature ↔ all CO₂ sensors | positive | Warming consistently drives gas upward |

---

## Why this matters

Before applying any signal processing, it is essential to confirm that the sensors are measuring the same physical phenomenon and not independent noise. The near-perfect cross-stack correlation proves that:

- The CO₂ gas blanket inside the mofette is **spatially homogeneous** horizontally at each height level.
- Environmental drivers (pressure and temperature) affect all sensor positions **consistently** — there is no isolated rogue sensor.
- The top sensors' lower correlation is physically meaningful: they sit at the **gas–air boundary layer** and are influenced by wind mixing from the outside.

This validation step justifies treating any single representative sensor as a proxy for the full horizontal layer when performing DSP analysis in later slides.
