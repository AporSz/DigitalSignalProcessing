# Slide 15 – Drivers: Pressure & Temperature

## What this slide shows

This slide answers the key causal question of the study: **what physical forces make the mofette breathe?**

Two **cross-correlation plots** are shown stacked vertically:

1. **dsp_06_xcorr_pressure.png** — cross-correlation between CO₂ concentration and atmospheric (barometric) pressure.  
2. **dsp_07_xcorr_temperature.png** — cross-correlation between CO₂ concentration and ambient air temperature.

Cross-correlation is computed on the **bandpass-filtered** diurnal signal (from Slide 12), so seasonal effects are removed and only the daily cycle is being compared.

---

## How cross-correlation works here

The cross-correlation function (XCF) measures the **linear similarity between two signals as one is shifted in time** relative to the other. A peak in the XCF at lag = τ means:

> Signal A at time *t* is most strongly related to Signal B at time *t + τ*.

In other words, the lag tells us **which signal leads and which follows** — a critical distinction for establishing causality.

---

## Key findings

### Barometric Pressure (dsp_06_xcorr_pressure.png)

| Metric | Value |
|---|---|
| Peak correlation | **r = −0.42** |
| Lag at peak | ~0 hours |
| Direction | Negative |

- The **negative correlation** means that when atmospheric pressure *rises*, CO₂ concentration *falls*, and vice versa.
- The **near-zero lag** means this response is essentially instantaneous — the mofette reacts to pressure changes within the measurement resolution (minutes to hours).
- **Physical mechanism:** The atmosphere acts like a piston. Higher pressure pushes down on the gas pool, compressing it back into the vent. Lower pressure releases that force, allowing the CO₂ to expand upward and flood more of the stack.

### Ambient Temperature (dsp_07_xcorr_temperature.png)

| Metric | Value |
|---|---|
| Peak correlation | **r = +0.28** |
| Lag at peak | ~3 hours |
| Direction | Positive |

- The **positive correlation** means that warmer temperatures drive higher CO₂ concentrations in the boundary layer.
- The **3-hour lag** means that CO₂ peaks approximately 3 hours *after* the temperature peaks.
- **Physical mechanism:** Sunlight heats the ground surface, which then warms the soil and gas below through conduction. This thermal inertia introduces the observed 3-hour delay before the gas expands enough to push the boundary layer upward.

---

## Why this matters

These two cross-correlations constitute the **physical model** of the mofette in miniature:

```
Pressure drop  →  (0 h delay)  →  CO₂ rises
Temperature rise  →  (3 h delay)  →  CO₂ rises
```

This has direct practical applications:

- **Short-term forecasting** — barometric pressure is one of the most accurate short-range weather forecast variables. Because CO₂ responds to pressure with zero lag, pressure forecasts can be used to predict gas level changes hours in advance.
- **Hazard management** — storm fronts (which bring rapid pressure drops) correspond to sudden surges in gas emission. Warning systems could trigger on forecast pressure drops.
- **Model validation** — any predictive model of the mofette must reproduce both of these correlations and their lags. Failure to do so would indicate a physically incorrect model.

The combined pressure + temperature picture also explains *why* the diurnal cycle peaks when it does: midday pressure typically rises while temperature peaks in early afternoon — their opposing and synergistic effects shape the asymmetric waveform observed in the bandpass output (Slide 12).
