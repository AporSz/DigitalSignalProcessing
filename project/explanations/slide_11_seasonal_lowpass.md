# Slide 11 – Seasonal Trends: Lowpass Filter

## What this slide shows

This slide presents the result of applying a **Butterworth lowpass filter** to the raw CO₂ time series from the boundary-layer sensor (sensor 10, at ~50 cm height). The plot (`dsp_03_lowpass_trend.png`) overlays the raw signal (grey/blue) with the extracted seasonal trend (red).

---

## Filter design

| Parameter | Value |
|---|---|
| Filter type | Butterworth (3rd order) |
| Cutoff period | **3 days** |
| Cutoff frequency | ≈ 3.86 × 10⁻⁶ Hz |
| Implementation | `sosfiltfilt` (zero-phase, SciPy) |

A 3-day cutoff means that any oscillation faster than 3 days (including the daily 24-hour cycle) is **removed**, leaving only the slow background trend.

---

## What the plot shows

- The **raw signal** (thin line) fluctuates rapidly up and down with the daily breathing rhythm. The seasonal envelope is difficult to see through the noise.
- The **lowpass output** (thick red line) is a smooth curve that tracks the underlying baseline level of CO₂ at that height.

### Seasonal behaviour
| Season | Observed trend |
|---|---|
| Spring (May–Jun) | Moderate CO₂ baseline, rising |
| Summer (Jul–Aug) | Peak baseline — the gas blanket rises highest |
| Autumn (Sep–Oct) | Declining baseline as temperatures drop |

The summer peak in the trend correlates with increased soil heating and regional atmospheric pressure patterns typical of warm months.

---

## Why this matters

The lowpass trend answers a fundamental question: **does the mofette's overall activity level change across the year?**

The answer is yes — the baseline CO₂ concentration at the boundary sensor is not constant but follows a clear seasonal arc. This has practical implications:

- Safety assessments of the mofette site (for visitors or nearby infrastructure) must account for **elevated danger in summer months** when the gas layer sits higher and covers more volume.
- Predictive models trained on this data must include a seasonal component to avoid systematic errors.
- The trend also validates the geological premise: the mofette responds to macroscopic environmental forcing (temperature, pressure), not just local instrument noise.

The extracted trend component will be **subtracted** before bandpass analysis in the next slide, ensuring that the diurnal cycle is examined in isolation.
