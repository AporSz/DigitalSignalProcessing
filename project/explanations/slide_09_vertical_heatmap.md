# Slide 9 – Spatial Dynamics: Vertical Heatmap

## What this slide shows

This slide introduces the **spatial dimension** of the mofette's CO₂ dynamics through a vertical heatmap (`10_CO2_heatmap.png`).

- **X-axis:** Time (spanning the full 7-month measurement campaign).  
- **Y-axis:** Height above the mofette floor, from 0 cm (bottom of the stack) to 95 cm (top sensor).  
- **Colour scale:** CO₂ concentration — blue (≈ 0%, fresh air) to red (≈ 100%, pure CO₂).

---

## What the heatmap reveals

| Zone | Height | Behaviour |
|---|---|---|
| **Permanent saturation layer** | 0 – 30 cm | Constant deep red — near-100% CO₂ at all times |
| **Dynamic boundary layer** | 40 – 60 cm | Oscillating colours — the interface between pure gas and fresh air |
| **Air zone** | 60 – 95 cm | Mostly blue — fresh atmospheric air |

### Seasonal pattern
The boundary layer height is **not static across the year**. It rises noticeably higher into the stack during mid-summer, reflecting increased geothermal activity and solar heating that drives more gas upward.

### Daily pattern
Even at the heatmap's time resolution, a fine vertical oscillation is visible in the boundary zone — the day-night breathing cycle that will be examined in detail using digital filters in Slides 11 and 12.

---

## Why this matters

The vertical heatmap is the single most intuitive visualisation in the presentation because it makes the **physical structure of the mofette immediately visible**:

1. **Layered stratification** — CO₂ is heavier than air and naturally sinks, forming a stable dense layer at the bottom.
2. **Breathing interface** — the middle boundary layer is where all the interesting dynamics happen. It expands and contracts in response to both environmental drivers (pressure and temperature) and geological activity.
3. **Motivation for spatial filtering** — because different heights behave differently, analyses in subsequent slides focus on a specific representative height (sensor at ~50 cm, sensor index 10) that sits squarely in the active boundary zone.

This slide sets up the narrative for *why* signal decomposition (Slide 10) is needed: the boundary layer mixes slow seasonal drifts with fast daily oscillations simultaneously.
