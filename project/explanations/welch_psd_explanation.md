# Explanation of Slide 13: Frequency Domain (Welch's PSD)

This document provides a detailed scientific explanation of **Slide 13: "Mathematical Proof: Welch's PSD"** in the presentation deck. It covers the digital signal processing (DSP) methodologies, the plot axes, and the physical mechanisms driving the observed signals.

---

## 1. What is Power Spectral Density (PSD)?
The **Power Spectral Density (PSD)** is a frequency-domain representation of a time-series signal. It describes how the total power (or variance) of a signal is distributed over different frequencies.
*   **Units:** Since the carbon dioxide concentration is measured in percentage ($\%$), the variance is in $\%^2$, and the PSD is expressed in **$(\%^2)/\text{Hz}$** (variance per unit frequency).
*   **Significance:** Higher values (peaks) on the PSD curve indicate that the signal possesses strong periodic components at those specific frequencies. It allows us to distinguish true cyclic behaviors from random, non-periodic background noise.

---

## 2. Why Use Welch's Method?
The raw mofette campaign dataset spans 200 days of active recording, yielding over 17 million data points. A direct Fast Fourier Transform (FFT) of the entire signal (a raw periodogram) would result in a highly noisy spectrum with excessive variance (making it look like a jagged, unreadable block of noise).

To solve this, **Welch's Method** (averaged periodograms) is used:
1.  **Segmentation:** The long signal is split into overlapping segments. For this analysis, we used a **7-day window segment** (10,080 minutes) with **50% overlap**.
2.  **Windowing:** A Hann window is applied to each segment. This tapers the signal at the edges, preventing spectral leakage (computational distortion at the boundaries of the segments).
3.  **Averaging:** The FFT magnitude squared is calculated for each segment, and all resulting spectra are averaged together. 
*   **Result:** Averaging reduces the variance of the spectral estimate by a factor of $K$ (the number of segments), smoothing out random noise and revealing the underlying periodic peaks.

---

## 3. Explaining the Plot Features (Figure 5)

### Log-Log Scale
Both axes are plotted on a logarithmic scale. This is necessary because the signal power ranges over several orders of magnitude (from highly dominant daily cycles down to tiny millihertz sensor noise), and the periods range from 1 hour to over a week.

### Inverted X-Axis (Period in Hours)
Standard spectral plots display frequency on the x-axis, increasing to the right. Since frequency ($f$) and period ($T$) are inversely related ($T = 1/f$), this makes the x-axis difficult to read in time units.
*   By converting frequency to period (in hours) and **inverting the x-axis**, the plot keeps the standard visual convention (long-term slow cycles on the left, fast noise on the right) while labeling the ticks in intuitive hours (e.g., 24h, 12h, 8h).

### The 24-Hour Peak
The absolute dominant feature on the plot is a massive, sharp spike at exactly **24 hours**. This represents the fundamental frequency of the system.

### The 12-Hour and 8-Hour Harmonics
Smaller but distinct secondary peaks are visible at exactly **12 hours** and **8 hours**.
*   In signal processing, a pure sinusoidal wave has only a single peak at its fundamental frequency.
*   If the periodic wave is non-sinusoidal (e.g., has sharp transitions, or is flat at the top/bottom due to sensor saturation), it decomposes into a fundamental frequency ($f$) and integer harmonics ($2f$, $3f$, etc.).
*   The second harmonic corresponds to $2 \times (1/24\text{ h}) = 1/12\text{ h}$ (12-hour period).
*   The third harmonic corresponds to $3 \times (1/24\text{ h}) = 1/8\text{ h}$ (8-hour period).
*   The presence of these peaks mathematically proves that the mofette's daily cycle is asymmetric and non-sinusoidal.

---

## 4. Physical Mechanisms (The "Why")

*   **Solar/Diurnal Ventilation (24h Peak):** The daily breathing rhythm is driven by solar heating.
    *   **Nighttime Accumulation:** As the ground cools and the air column stabilizes under low-wind conditions, the heavy CO₂ gas ($\sim 1.5$ times the density of air) pools inside the mofette. This raises the concentration at the 50 cm sensor (Sensor 10) to nearly 100%.
    *   **Daytime Dilution:** Sun heating warms the ground, inducing convective currents and wind that mix and dilute the CO₂ blanket with ambient air.
*   **Day/Night Transition Asymmetry (12h & 8h Peaks):** The presence of harmonics indicates that the morning ventilation (driven by quick solar heating and wind onset) happens much faster than the slow, gravity-driven accumulation of gas in the evening. This creates a non-sinusoidal, asymmetric wave.
