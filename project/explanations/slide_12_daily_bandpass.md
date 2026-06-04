# Slide 12 – Isolating the Daily Cycle: Bandpass Filter

## What this slide shows

This slide presents the result of applying a **Butterworth bandpass filter** to extract the 24-hour diurnal breathing oscillation from the CO₂ signal. The plot (`dsp_04_bandpass_daily.png`) contains two panels:

1. **Full 7-month view** — the isolated diurnal component across the entire campaign.  
2. **2-week zoomed view** — a close-up revealing the shape and regularity of the daily cycle.

---

## Filter design

| Parameter | Value |
|---|---|
| Filter type | Butterworth (bandpass) |
| Passband | **18 hours to 30 hours** |
| Low cutoff frequency | ≈ 1.54 × 10⁻⁵ Hz |
| High cutoff frequency | ≈ 9.26 × 10⁻⁶ Hz |
| Implementation | `sosfiltfilt` (zero-phase, SciPy) |

The 18–30 hour passband is centred on 24 hours and is wide enough to capture the full energy of the daily cycle while rejecting both the slow seasonal trend (period >> 30 h) and any high-frequency sensor noise (period << 18 h).

---

## What the plots show

### Full 7-month panel
- The filtered signal oscillates continuously throughout the entire measurement period, confirming that the daily breathing cycle is **persistent and never disappears**.
- The **amplitude of the oscillation varies seasonally** — it is noticeably larger in summer (July–August) than in spring or autumn, consistent with the stronger solar forcing in summer months.

### 2-week zoomed panel
- The zoomed view reveals a highly **regular, near-sinusoidal waveform** with a period of almost exactly 24 hours.
- The blue line (raw detrended signal) and green line (bandpass output) track each other very closely, indicating that the 24-hour oscillation dominates the signal in this frequency band.
- Slight asymmetry between the rising and falling edges of the wave reflects the non-sinusoidal nature of the thermal drive (daytime heating is faster than night-time cooling).

---

## Why this matters

Isolating the diurnal cycle is the core DSP achievement of this study. It allows:

1. **Precise amplitude measurement** — quantifying how much CO₂ level changes from day-night, as a pure oscillation stripped of seasonal bias.
2. **Waveform shape analysis** — the slight non-sinusoidal shape (also visible as harmonics in the PSD on Slide 13) gives information about whether the gas responds linearly to temperature.
3. **Cross-correlation with drivers** — once isolated, this clean diurnal signal can be compared directly with atmospheric pressure and temperature to determine which factor drives the breathing and by how much (Slide 15).

The regular, stable diurnal wave visible in the 2-week zoom is one of the most compelling results of the study: it shows that the mofette breathes like clockwork, driven by predictable daily environmental cycles.
