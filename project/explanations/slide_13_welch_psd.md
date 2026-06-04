# Slide 13 – Mathematical Proof: Welch's PSD

## What this slide shows

This slide provides **frequency-domain confirmation** of the 24-hour breathing cycle using **Welch's Power Spectral Density (PSD)** method. The plot (`dsp_01_PSD_welch.png`) shows spectral power (Y-axis, in dB or linear power units) against oscillation period (X-axis, in hours), for sensor 10 (the boundary-layer sensor at ~50 cm).

> For a detailed mathematical explanation of the Welch method itself, see [`welch_psd_explanation.md`](./welch_psd_explanation.md).

---

## Welch's method — brief recap

Standard Fourier transforms applied to a 7-month raw signal would produce a very noisy spectrum because a single CO₂ measurement contains sensor noise and irregular transients. **Welch's method** reduces this variance by:

1. Splitting the signal into **overlapping segments** (7-day window, 50% overlap).
2. Applying a **window function** (typically Hann) to each segment to reduce spectral leakage.
3. Computing the FFT of each segment and **averaging the power spectra**.

The result is a much smoother spectrum with genuine peaks rising clearly above the noise floor.

---

## What the plot shows

| Peak | Period | Interpretation |
|---|---|---|
| **Primary (dominant)** | **24 hours** | The fundamental diurnal breathing frequency |
| Secondary | 12 hours | 2nd harmonic — reflects the non-sinusoidal shape of the daily cycle |
| Tertiary | 8 hours | 3rd harmonic — further asymmetry between day and night |

### The 24-hour peak
The 24-hour peak towers above all others by several orders of magnitude. This **mathematically confirms** — without any prior assumption — that the dominant periodicity of CO₂ fluctuation at this height is exactly one solar day.

### Harmonics
The presence of 12-hour and 8-hour harmonics indicates that the daily cycle is not a pure sine wave. A pure sine would produce only a single spectral line. The harmonics arise because the CO₂ response to temperature and pressure is slightly asymmetric: the gas rises more abruptly during daytime heating than it settles during night-time cooling.

---

## Why this matters

Welch's PSD serves as the **objective, model-free proof** of periodicity. Unlike the bandpass filter (Slide 12), which was specifically designed to find the 24-hour cycle, the PSD makes no assumptions about what frequencies are present — it simply measures what is there.

This distinction is scientifically important:

- The filter was designed *because* we hypothesised a 24-hour cycle (based on physical reasoning and visual inspection).
- The PSD independently *verifies* that hypothesis from the data alone.

The harmonics also provide additional information: they tell us that a simple sinusoidal model of mofette breathing would be an approximation, and that higher-fidelity models (Slide 16) should include non-linear response terms.
