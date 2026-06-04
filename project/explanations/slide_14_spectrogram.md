# Slide 14 – Spectrogram: Time-Frequency View

## What this slide shows

While the Welch PSD (Slide 13) shows *which* frequencies are present across the entire 7-month campaign, this slide answers a different question: **does the strength of those frequencies change over time?**

The spectrogram (`dsp_05_spectrogram.png`) answers this by computing the PSD in a **sliding 7-day window** moving in 1-day increments across the full campaign.

- **X-axis:** Calendar time (the 7-month campaign).  
- **Y-axis:** Oscillation period in hours (ranging from 6 h to 72 h).  
- **Colour:** Power — dark = low energy, bright/yellow = high energy.  
- **White dashed line:** Marks the exact 24-hour period for reference.

---

## What the spectrogram reveals

### The 24-hour ridge
A continuous, bright horizontal band runs along the entire X-axis at the 24-hour mark. This confirms that the diurnal breathing cycle is **not a transient event** — it is present every single day throughout the measurement period.

### Seasonal amplitude modulation
The brightness of the 24-hour ridge is **not uniform across time**:

| Period | Band brightness | Interpretation |
|---|---|---|
| May–June | Moderate | Spring — moderate solar forcing |
| July–August | **Brightest** | Summer — strong solar heating amplifies daily amplitude |
| September–October | Fading | Autumn — cooling reduces diurnal forcing |

This seasonal modulation of the diurnal cycle's strength is one of the most important findings of the study: it shows that the mofette's breathing *rhythm* stays constant (always 24 h) but its *intensity* is controlled by seasonal solar energy input.

### Other periods
Below the 24-hour line, faint bands at 12 h and 8 h are visible — these are the harmonics also seen in the PSD (Slide 13), confirming that the non-sinusoidal waveform shape persists throughout the year.

---

## Why this matters

The spectrogram adds the **time dimension** to the frequency analysis. This is crucial because:

1. **Stationarity check** — a core assumption of many signal processing methods is that the signal's statistical properties do not change over time (stationarity). The spectrogram reveals that this assumption is *partially violated* — the amplitude varies seasonally, even though the period does not. This is important context for any future modelling work.

2. **Physical interpretation** — the peak intensity in August–September aligns with the hottest, sunniest months in Romania. This links the mofette's behaviour directly to solar irradiance, not just local temperature, suggesting that the energy budget of the region's surface drives the gas dynamics.

3. **Predictive value** — because the intensity of breathing is predictable from the season, forecasting models can use the time of year as an additional input variable to improve accuracy.

Together, Slides 13 and 14 form a complete frequency-domain portrait of the mofette signal: the PSD shows the *what*, and the spectrogram shows the *when and how much*.
