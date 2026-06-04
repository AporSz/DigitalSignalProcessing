# CO₂ Dynamics in a Mofette: DSP & Tectonic Analysis Explanations

This document provides a detailed explanation of the digital signal processing (DSP) methods and geological mapping refinements used in the mofette carbon dioxide emission research project in Covasna, Romania. It is designed to be shared with colleagues and collaborators.

---

## 1. Tectonic Map Calibration: Relocating the Covasna Marker

### The Problem
During the integration of map resources, the initial marker for Covasna was placed at coordinates $X = 492, Y = 290$ on the tectonic plates map of Romania. While this placed it in the correct latitude range, it was **too far east**, putting it in the outer sedimentary platform (**Moldavides zone**).

Geographically, Covasna is located in the Eastern Carpathians bend zone, just north-northeast of Brașov, right at the boundary where the flat Transylvanian basin meets the rising volcanic/crustal mountain arc.

### The Solution: Coordinate Registration
To align the tectonic plates map and the geographic/satellite map, we implemented a linear coordinate registration system using three major cities with known GPS coordinates and identifiable city circles on the tectonic map:

| City | Latitude ($^\circ\text{N}$) | Longitude ($^\circ\text{E}$) | Tectonic Map Pixel Coordinate ($X, Y$) |
| :--- | :--- | :--- | :--- |
| **Cluj-Napoca** | $46.77121$ | $23.62363$ | $(282, 213)$ |
| **Brașov** | $45.65797$ | $25.60120$ | $(450, 308)$ |
| **Bucharest** | $44.42677$ | $26.10254$ | $(567, 467)$ |

We modeled the transformation from geographic coordinates $(\text{Longitude}, \text{Latitude})$ to tectonic map pixel space $(X, Y)$ using a linear affine system:
$$X_{\text{tect}} = a \cdot \text{Lon} + b \cdot \text{Lat} + c$$
$$Y_{\text{tect}} = d \cdot \text{Lon} + e \cdot \text{Lat} + f$$

Solving this system using the reference coordinates yielded the mapping coefficients:
*   **For $X$:** $a = 40.8129, b = -78.4104, c = 2985.1978$
*   **For $Y$:** $d = -31.9934, e = -142.1699, f = 7618.2588$

### Corrected Coordinates
Applying these mapping coefficients to Covasna's exact GPS coordinates ($45.84278^\circ\text{ N}, 26.17722^\circ\text{ E}$):
$$X_{\text{Covasna}} \approx 459.02$$
$$Y_{\text{Covasna}} \approx 263.30$$

*   **Pixel Location:** $(459, 263)$
*   **Geological Position:** This matches perfectly with the green **Outer Dacides band** (representing the flysch zones of the Eastern Carpathians), placed right on the eastern edge of the basin indentation, northeast of Brașov.
*   **Action Taken:** The tectonic image (`romania_tectonic_plates.png`) was regenerated with the marker and label relocated to $(459, 263)$.

---

## 2. Frequency Domain Analysis: Welch's PSD (Slide 6)

### What is Power Spectral Density (PSD)?
A **Power Spectral Density** is a frequency-domain representation of a time-series signal. It shows the distribution of the signal's power (variance) across different frequencies. 
*   **Signal Units:** Since the sensor output measures CO₂ concentration in percentage ($\%$), the variance is in $\%^2$, and the PSD is expressed in **$(\%^2)/\text{Hz}$** (or cycles per time unit).
*   **Interpretation:** Peaks in the PSD plot highlight the dominant frequencies at which the gas concentrations oscillate.

### Why Welch's Method?
The raw dataset spans over 7 months at 1-second resolution, containing millions of points. Estimating the frequency spectrum using a standard raw periodogram (direct FFT of the entire signal) produces a spectrum with extremely high variance (very noisy and jagged), making it difficult to distinguish true physical periodicities from high-frequency sensor noise.

**Welch's Method** (averaged periodogram) improves the estimate by:
1.  **Segmentation:** Splitting the time series into overlapping segments. In our case, we used a **7-day window segment** (10,080 minutes) with **50% overlap**.
2.  **Windowing:** Applying a window function (Hann window) to each segment to prevent spectral leakage (distortion caused by cropping the signal).
3.  **Averaging:** Computing the FFT of each segment and then averaging the power spectra together.
*   This averaging dramatically reduces the variance, smoothing out the noise and yielding a clean, statistically robust estimate of the true periodic cycles.

### Understanding the Plot (Slide 6)
*   **Inverted X-axis (Period in Hours):** Typically, spectra plot frequency ($f$) on the x-axis, increasing to the right. However, frequency units like $1.15 \times 10^{-5}\text{ Hz}$ are hard to interpret. By converting frequency to period ($T = 1/f$ in hours) and **inverting the x-axis**, we keep the standard visual convention (long-term cycles/trends on the left, short-term fluctuations/noise on the right) while reading the x-axis in intuitive hours.
*   **The 24-Hour Peak:** There is a massive, sharp spike at exactly $T = 24 \text{ hours}$. This is the fundamental frequency of the signal and is the strongest peak in the entire spectrum.
*   **The 12-Hour and 8-Hour Harmonics:** Smaller, secondary spikes are visible at $12 \text{ hours}$ and $8 \text{ hours}$.

### Physical Interpretation
*   **Diurnal Ventilation (24h Peak):** The dominant 24-hour cycle is driven by the diurnal solar cycle. 
    *   **During the night**, thermal radiation cools the ground, wind speeds drop, and the atmospheric boundary layer stabilizes. Because CO₂ is heavy ($\sim 1.5$ times the density of air), it pools inside the mofette, rising past the 50 cm sensor (Sensor 10) to reach nearly 100% saturation.
    *   **During the day**, solar heating warms the ground, triggering convective air mixing and micro-winds that dilute the CO₂ blanket with ambient air.
*   **Non-Sinusoidal Breathing (12h & 8h Peaks):** If the mofette's breathing cycle were a perfect, symmetric sine wave, its spectrum would show only the 24-hour peak. 
    *   In Fourier theory, any periodic signal that is non-sinusoidal (e.g. flat-topped due to sensor saturation or showing asymmetric rise/fall slopes) decomposes into a fundamental frequency ($f$) and its integer harmonics ($2f, 3f, 4f...$).
    *   The second harmonic is at $2 \times (1/24\text{ h}) = 1/12\text{ h}$ (12-hour period).
    *   The third harmonic is at $3 \times (1/24\text{ h}) = 1/8\text{ h}$ (8-hour period).
    *   The presence of these harmonics mathematically proves that the day-to-night transitions are asymmetric. Convective dilution during the morning occurs at a faster rate than the gravity-driven pooling of gas in the evening.
