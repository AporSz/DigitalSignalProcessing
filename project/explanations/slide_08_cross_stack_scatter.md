# Slide 8 – Cross-Stack Scatter & Trendlines

## What this slide shows

This slide moves beyond correlation coefficients and **visualises the raw point-cloud relationship** between the main monitoring stack and the side tube using hexbin density scatter plots with linear trendlines overlaid.

Two plots are shown stacked vertically:

1. **temperature_main_vs_side.png** — temperature readings from the main stack (X-axis) vs. the side tube (Y-axis).  
2. **CO2_main_vs_side.png** — CO₂ concentration from the main stack vs. the side tube, with hexbin density colouring showing where most data points cluster.

---

## Key findings

| Variable | Pearson r | Interpretation |
|---|---|---|
| Temperature (Main vs. Side) | **0.981** | Near-perfect linear alignment — the thermal environment is spatially homogeneous |
| CO₂ (Main vs. Side) | **0.678** | Strong positive correlation — gas concentrations track each other despite spatial offset |

### Hexbin density insight
The hexbin colour map shows that the **majority of recordings cluster at high CO₂ values** (upper-right region of the scatter). This indicates that high-concentration conditions are the *norm*, not the exception — the stable CO₂ reservoir at the bottom of the mofette persists throughout the measurement campaign.

---

## Why this matters

The scatter + trendline approach complements the correlation matrix from Slide 7 by:

- **Visually confirming linearity** — a high correlation coefficient could theoretically be driven by a non-linear or clustered relationship. The scatter plot rules this out.
- **Quantifying the density distribution** — the hexbin plot reveals that the gas blanket is present most of the time, which is important for modelling steady-state conditions.
- **Validating instrument placement** — if the two stacks behaved very differently, spatial averaging would be invalid. These results confirm that either channel can be used as a representative sample.

This slide bridges the spatial validation of Slide 7 with the temporal analysis that follows in Slide 9.
