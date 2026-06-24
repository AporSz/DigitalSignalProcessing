# Digital Signal Processing: Transforms Cheatsheet

This cheatsheet covers the core mathematical transforms used in DSP, when to use them, their formulas, and how they mathematically relate to one another.

---

## 1. Continuous-Time Fourier Transform (CTFT)
*   **What it is:** Converts a continuous, infinite time-domain signal into a continuous frequency spectrum.
*   **When to use:** Analyzing pure analog signals in theory (e.g., finding the bandwidth of an analog filter).
*   **Formula:** $X(j\omega) = \int_{-\infty}^{\infty} x(t) e^{-j\omega t} dt$
*   **The Trick:** It assumes the signal is completely stable (doesn't blow up to infinity). If the signal grows exponentially, the integral fails to converge!

## 2. Laplace Transform
*   **What it is:** A generalized version of the CTFT for analog signals.
*   **When to use:** Analyzing **unstable** continuous systems, solving differential equations, or designing analog filters (S-plane analysis).
*   **Formula:** $X(s) = \int_{-\infty}^{\infty} x(t) e^{-st} dt$  *(where $s = \sigma + j\omega$)*
*   **The Trick:** The $\sigma$ term adds a mathematical damping factor ($e^{-\sigma t}$). This forces unstable, blowing-up signals to artificially converge so we can still analyze them!
*   **Relationship:** If you evaluate the Laplace transform purely on the imaginary axis (set $\sigma = 0$, so $s = j\omega$), it perfectly collapses back into the standard **CTFT**!

---

## 3. Discrete-Time Fourier Transform (DTFT)
*   **What it is:** Converts a discrete sampled signal ($x[n]$) into a continuous frequency spectrum.
*   **When to use:** Theoretical analysis of digital filters and sampled signals.
*   **Formula:** $X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$
*   **The Trick:** Because the input is sampled, the resulting frequency spectrum is **periodic**. The spectrum endlessly repeats itself every $2\pi$ radians (or every $f_s$ Hertz).

## 4. Z-Transform
*   **What it is:** A generalized version of the DTFT for digital signals (the discrete equivalent of Laplace).
*   **When to use:** Analyzing **unstable** digital systems, solving difference equations, and finding the transfer function $H(z)$ for digital filters (Z-plane analysis).
*   **Formula:** $X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n}$ *(where $z = r \cdot e^{j\omega}$)*
*   **The Trick:** The $r$ term adds a damping factor. It allows us to analyze growing digital signals by pulling them inside a Region of Convergence (ROC).
*   **Relationship:** If you evaluate the Z-Transform purely on the unit circle (set $r=1$, so $z = e^{j\omega}$), it perfectly collapses back into the standard **DTFT**!

---

## 5. Discrete Fourier Transform (DFT) / Fast Fourier Transform (FFT)
*   **What it is:** Converts a finite, discrete signal into a finite, discrete frequency spectrum.
*   **When to use:** **Any real-world computer code!** Computers cannot handle continuous math or infinite arrays, so we use the FFT to calculate frequency bins.
*   **Formula:** $X[k] = \sum_{n=0}^{N-1} x[n] e^{-j 2\pi k n / N}$
*   **The Trick:** The DFT fundamentally assumes your finite chunk of data loops perfectly forever. If the ends don't line up, it causes **Spectral Leakage**. Always use a Window function!
*   **Relationship:** The DFT is simply taking the continuous DTFT spectrum and sampling it at $N$ discrete points around the unit circle. The FFT is just an insanely fast algorithm ($O(N \log N)$) to calculate the DFT.

---

## 6. Short-Time Fourier Transform (STFT) / Spectrogram
*   **What it is:** Chops a long signal into small overlapping time chunks and runs an FFT on each chunk.
*   **When to use:** Analyzing signals where the frequencies change over time (e.g., Speech, Music, EEG).
*   **The Trick:** You are bound by the **Uncertainty Principle**. If you use a long time chunk, you get great frequency resolution but blurry time resolution. If you use a short chunk, you get great time resolution but blurry frequencies. You cannot have both!

## 7. Continuous Wavelet Transform (CWT)
*   **What it is:** Convolves the signal with a mathematically generated "wavelet" that is stretched and squashed to hunt for different frequencies.
*   **When to use:** When you need to escape the Uncertainty Principle of the STFT! Perfect for finding sudden spikes (like heartbeats or brain waves).
*   **The Trick:** Because the wavelet dynamically stretches, it gives you **excellent time resolution** for high frequencies (sharp spikes) and **excellent frequency resolution** for low frequencies (slow rumbles) simultaneously!

---

## 🔗 The Master Map of Relationships
1. **Sampling:** When you physically sample a continuous signal (CTFT), its frequency spectrum infinitely duplicates itself to become a DTFT. (This is why Nyquist aliasing exists!).
2. **The S-Plane to Z-Plane Bridge:** The **Bilinear Transform** ($s = \frac{2}{T} \frac{z-1}{z+1}$) takes the entire stable left-half of the continuous Laplace S-plane and violently wraps it so it fits perfectly inside the stable unit circle of the discrete Z-plane.
3. **Axis Collapsing:**
   * Laplace ($S$-plane) evaluated on the imaginary axis $\rightarrow$ CTFT.
   * Z-Transform ($Z$-plane) evaluated on the unit circle $\rightarrow$ DTFT.
   * DTFT sampled at discrete points $\rightarrow$ DFT (FFT).
