# Digital Signal Processing: Filter Design Cheatsheet

This cheatsheet covers the three primary filter design methods, the mathematical steps to execute them, and the `scipy.signal` Python functions required.

---

## 1. The Bilinear Transform (IIR Filters)
**Type:** Infinite Impulse Response (IIR)
**Pros:** No aliasing! Can be used for Low-Pass, High-Pass, Band-Pass, and Band-Stop.
**Cons:** Causes severe "Frequency Warping" at high frequencies near the Nyquist limit.

### The Steps:
1. **Define Specs:** Determine your sampling frequency ($f_s$) and your desired digital cutoff frequency ($f_c$).
2. **Pre-warping:** Calculate the artificially stretched analog frequency ($\Omega_c$) to counteract the Bilinear crushing effect: 
   $$\Omega_c = 2 f_s \tan\left(\pi \frac{f_c}{f_s}\right)$$
3. **Analog Prototype:** Design an analog filter (like a Butterworth) using your new pre-warped $\Omega_c$.
4. **Bilinear Transform:** Convert the analog $H(s)$ into a digital $H(z)$ using the $s = \frac{2}{T} \frac{z-1}{z+1}$ substitution.
5. **Apply Filter:** Apply the filter to your signal in the time domain using forward-backward filtering to preserve phase.

### Python Functions (`scipy.signal`):
*   **Analog Prototype:** `b, a = signal.butter(order, prewarped_Wn, btype='lowpass', analog=True)`
*   **Bilinear Transform:** `bz, az = signal.bilinear(b, a, fs=fs)`
*   **Frequency Response (Digital):** `wz, hz = signal.freqz(bz, az, fs=fs)`
*   **Apply Filter (Time Domain):** `filtered_signal = signal.filtfilt(bz, az, data)`

---

## 2. Impulse Invariance Method (IIR Filters)
**Type:** Infinite Impulse Response (IIR)
**Pros:** Preserves the exact shape of the continuous-time impulse response and preserves phase.
**Cons:** Suffers from severe **Aliasing**. Because of this, it can **ONLY** be used for Low-Pass or Band-Pass filters. It is completely useless for High-Pass filters!

### The Steps:
1. **Analog Prototype:** Start with an analog transfer function $H_a(s)$.
2. **Inverse Laplace:** Perform Partial Fraction Expansion and use the Inverse Laplace Transform to find the continuous impulse response $h_a(t)$.
3. **Sample It:** Digitally sample that continuous equation at every $T_s$ seconds to get your discrete sequence $h[n] = h_a(n T_s)$.
4. **Z-Transform:** Apply the Z-transform to $h[n]$ to get your final digital transfer function $H(z)$.

### Python Functions (`scipy.signal`):
*   *(While you usually do the math by hand on exams, Python can automate it)*
*   **Impulse Invariance:** `bz, az = signal.cont2discrete((b, a), dt=1/fs, method='impulse')`

---

## 3. Fourier / Window Method (FIR Filters)
**Type:** Finite Impulse Response (FIR)
**Pros:** Can easily achieve **perfect linear phase** (no time distortion). Always strictly stable.
**Cons:** Requires many more filter taps (more memory/CPU) than IIR to achieve a steep cutoff.

### The Steps:
1. **Ideal Response:** Define your perfect, ideal frequency response (e.g., a perfect rectangle for a Low-Pass).
2. **Inverse Fourier:** Calculate the Inverse Discrete-Time Fourier Transform (IDTFT) to get the ideal time-domain impulse response ($h_{ideal}[n]$), which will be an infinite `sinc` wave.
3. **Truncate:** Chop the infinite signal down to a finite number of samples (length $N$).
4. **Apply Window:** To prevent the **Gibbs Phenomenon** (which causes massive frequency ripples when you chop a signal abruptly), multiply your chopped signal by a **Window Function** (Hamming, Hanning, Blackman). This smoothly tapers the edges down to zero.
5. **Final Filter:** $h[n] = h_{ideal}[n] \times w[n]$

### Python Functions (`scipy.signal`):
*   **Design FIR Filter:** `taps = signal.firwin(numtaps=N, cutoff=fc, window='hamming', fs=fs)`
    *(Note: `firwin` automatically handles the ideal sinc generation, truncation, and windowing all in one step!)*
*   **Frequency Response (FIR):** `w, h = signal.freqz(taps, [1.0], fs=fs)`
*   **Apply Filter (Time Domain):** `filtered_signal = signal.lfilter(taps, [1.0], data)` or `signal.filtfilt(...)`
