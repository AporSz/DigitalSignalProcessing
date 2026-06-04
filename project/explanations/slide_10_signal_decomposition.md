# Slide 10 – Our Approach: Signal Decomposition

## What this slide shows

This slide is a **methodological bridge** — it explains *why* raw signal analysis alone is insufficient and *how* digital signal processing (DSP) solves the problem. It contains no plots; instead it presents the analytical challenge and the chosen solution side-by-side.

---

## The analytical challenge

A raw CO₂ time series from the boundary layer (e.g. sensor at 50 cm) contains **two fundamentally different signals superimposed**:

| Component | Timescale | Physical cause |
|---|---|---|
| **Seasonal drift** | Weeks to months | Gradual geological and soil heating as seasons change |
| **Diurnal breathing** | ~24 hours | Daily temperature and pressure cycles |

Trying to analyse these together obscures the physical drivers of each. For example:

- A rising baseline trend in summer makes the daily peaks appear larger, even if the daily amplitude is unchanged.
- Cross-correlation with pressure would mix the slow trend's correlation with the fast cycle's correlation, producing a misleading averaged result.

---

## The digital filtering solution

To separate these two components cleanly, two **Butterworth filters** were designed and applied using SciPy's `sosfiltfilt` (zero-phase, forward-backward pass):

| Filter type | Cutoff / Passband | Isolates |
|---|---|---|
| **Lowpass** | Period > 3 days | Long-term seasonal trend |
| **Bandpass** | 18 h – 30 h (centred on 24 h) | Daily diurnal breathing cycle |

### Why zero-phase filtering?
Standard single-pass filters introduce a **phase delay** — they shift the output forward in time. This would mean that, for example, a pressure drop appears to *follow* a CO₂ rise when in reality it precedes it. Using `sosfiltfilt` applies the filter twice (once forward, once backward), which cancels the phase distortion and guarantees that **peaks in the filtered signal align exactly with peaks in the original**.

---

## Why this matters

This slide justifies the entire DSP portion of the presentation (Slides 11–15). Without signal decomposition:

- Seasonal and diurnal effects would be conflated.
- Cross-correlation with environmental drivers would be ambiguous.
- The spectrogram would not reveal the clean 24-hour energy peak.

By separating the two scales, the analysis can independently characterise the **long-term geological behaviour** (Slide 11) and the **short-term atmospheric-driven breathing** (Slides 12–15).
