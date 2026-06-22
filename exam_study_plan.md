# 📚 DSP Exam Study Plan — June 8 → June 23

> **Exam date:** Tuesday, June 23  
> **Phase 1 (Jun 8–16):** ~2 hours/day — Light review & concept refreshing  
> **Phase 2 (Jun 17–22):** ~8 hours/day — Deep study, practice problems, weak-area drilling  
> **June 23:** Exam day

---

## 🔍 Skill Gap Analysis

Based on your completed homework (hw1–hw9), here's your current standing:

| Area | Strength | Notes |
|---|---|---|
| Python basics, plotting | ✅ Strong | hw1–hw2 completed with code |
| Convolution (discrete) | ✅ Good | hw2 done |
| Fourier Transform (continuous FT) | ✅ Good | hw3 completed |
| Sampling, aliasing, reconstruction | ✅ Good | hw4–hw5 — solid aliasing demo code, good conceptual answers |
| FFT, zero-padding, DFT | ✅ Good | hw6 — correct understanding of zero-padding |
| Welch's PSD, periodogram, bias-variance | ✅ Good | hw7 — strong conceptual answers |
| Laplace transform, poles/zeros, Bode | ✅ Good | hw8 — solid grasp of stability, pole-zero analysis |
| Filters & LTI relationship | ⚠️ Partial | hw9 — only 1 question answered out of likely many |
| **Z-transform, digital filters** | ❌ **Not done** | hw10 — missing entirely |
| **Notch filter design** | ❌ **Not done** | hw11 — missing entirely |
| **Classical digitised filters (Butterworth, etc.)** | ❌ **Not done** | hw12 — missing entirely |

> [!WARNING]
> **Your biggest gap is the z-transform → digital filter design pipeline (hw10–12, Labs 10–13, Lectures 9–13).** This covers roughly 30–40% of a typical DSP exam. The study plan front-loads conceptual review in Phase 1 so that Phase 2 can focus heavily on these weak areas.

---

## Course Content Map

| # | Lecture (dspXX.pdf) | Lab | Homework |
|---|---|---|---|
| 01 | Intro to DSP, signals & systems | Python basics | hw1: Python exercises |
| 02 | Convolution, LTI systems | Discrete convolution | hw2: Convolution problems |
| 03 | Fourier Transform (continuous) | FFT lab: numerical FT approximation | hw3: FT exercises |
| 04 | FT properties (time-shift, etc.) | Time-shift property of FT | hw4: Aliasing demo |
| 05 | Sampling theorem, aliasing | Sampling & reconstruction | hw5: Sampling/reconstruction |
| 06 | DFT, FFT algorithm | Fast Fourier Transform | hw6: FFT, zero-padding |
| 07 | Power Spectral Density | Welch's PSD method | hw7: Periodogram, Welch |
| 08 | Laplace transform, Bode plots | Bode plots (continuous) | hw8: Poles/zeros, Bode, stability |
| 09 | Z-transform | Z-plane, stability, ROC | hw9: Filters & LTI |
| 10 | Digital filter design | Impulse response of LTI systems | hw10: ❌ NOT DONE |
| 11 | Notch/bandpass filter design | Manual notch filter design | hw11: ❌ NOT DONE |
| 12 | Classical digitised filters | Butterworth, Chebyshev, audio filtering | hw12: ❌ NOT DONE |
| 13 | Wavelets | Continuous wavelets | — |

---

## Phase 1: Light Review (2 hours/day)

### 📅 Day 1 — Monday, June 8
**Topic: Foundations — Signals, Systems & Convolution**

| Time | Activity |
|---|---|
| 0:00–0:40 | Re-read **Lecture 1** (dsp01.pdf) — signals, systems classification (causal, linear, time-invariant), energy vs. power signals |
| 0:40–1:10 | Re-read **Lecture 2** (dsp02.pdf) — convolution definition, properties (commutativity, associativity), impulse response |
| 1:10–1:30 | Re-run **Lab 02** notebook — discrete convolution exercises. Verify you can hand-compute a short convolution |
| 1:30–2:00 | Review your **hw1 & hw2** solutions. Redo any exercises you got wrong or feel unsure about |

**Self-test:** Can you compute `[1, 2, 3] * [1, 1]` by hand? Can you state the 3 conditions for an LTI system?

---

### 📅 Day 2 — Tuesday, June 9
**Topic: Fourier Transform — Continuous**

| Time | Activity |
|---|---|
| 0:00–0:50 | Re-read **Lecture 3** (dsp03.pdf) — continuous FT definition, inverse FT, magnitude/phase spectrum |
| 0:50–1:20 | Re-read **Lecture 4** (dsp04.pdf) — FT properties: linearity, time-shift, frequency-shift, Parseval's theorem |
| 1:20–1:45 | Re-run **Lab 03** — reproducing analytical FT with Python FFT |
| 1:45–2:00 | Review **hw3** solution. Write down the 5 most important FT properties from memory |

**Self-test:** What happens to the FT magnitude when you time-shift a signal? What does Parseval's theorem state?

---

### 📅 Day 3 — Wednesday, June 10
**Topic: Sampling, Aliasing & Reconstruction**

| Time | Activity |
|---|---|
| 0:00–0:50 | Re-read **Lecture 5** (dsp05.pdf) — Nyquist theorem, sampling frequency, aliasing, anti-aliasing filter, reconstruction |
| 0:50–1:20 | Re-run **Lab 05** — sampling and reconstruction exercises |
| 1:20–1:45 | Review your **hw4** code (aliasing demo) and **hw5** answers. Make sure you can draw the sampling/reconstruction pipeline from memory |
| 1:45–2:00 | Practice: Given f_signal = 7 Hz and f_sample = 10 Hz, what is the alias frequency? Draw the frequency-domain picture |

**Self-test:** Why do we need both an anti-aliasing filter AND a reconstruction filter? What's the minimum sampling rate for a 4 kHz signal?

---

### 📅 Day 4 — Thursday, June 11
**Topic: DFT, FFT & Zero-Padding**

| Time | Activity |
|---|---|
| 0:00–0:50 | Re-read **Lecture 6** (dsp06.pdf) — DFT definition, relationship to continuous FT, FFT algorithm (Cooley-Tukey), computational complexity O(N log N) |
| 0:50–1:20 | Re-run **Lab 06** — FFT exercises |
| 1:20–1:45 | Review **hw6** answers. Make sure you understand: zero-padding does NOT increase frequency resolution — it only interpolates between existing frequency bins |
| 1:45–2:00 | Practice: Given N=8 samples at fs=100 Hz, what are the DFT frequency bins? What is the frequency resolution? |

**Self-test:** What is the frequency resolution Δf for a signal of length T seconds? What does zero-padding actually do vs. collecting more data?

---

### 📅 Day 5 — Friday, June 12
**Topic: Power Spectral Density & Welch's Method**

| Time | Activity |
|---|---|
| 0:00–0:50 | Re-read **Lecture 7** (dsp07.pdf) — periodogram, bias-variance tradeoff, windowing (Hann, Hamming), Welch's method |
| 0:50–1:20 | Re-run **Lab 07** — implement Welch's PSD step-by-step |
| 1:20–1:50 | Review **hw7** answers thoroughly. Your answers are good but question 7 ("why does Welch reduce variance?") appears incomplete — make sure you can answer it: *averaging K independent periodograms reduces variance by factor 1/K* |
| 1:50–2:00 | Write a 1-paragraph summary of Welch's method from memory |

**Self-test:** Why is the periodogram inconsistent? What are the 7 steps of Welch's method? Why does overlap help?

---

### 📅 Day 6 — Saturday, June 13
**Topic: Laplace Transform & Continuous-Time Systems**

| Time | Activity |
|---|---|
| 0:00–0:50 | Re-read **Lecture 8** (dsp08.pdf) — Laplace transform, transfer function H(s), poles & zeros, ROC, stability criteria |
| 0:50–1:20 | Re-read **Lecture 9** (dsp09.pdf) — begin z-transform concepts |
| 1:20–1:50 | Re-run **Lab 08** — Bode plots. Review **hw8** answers (these are strong) |
| 1:50–2:00 | Practice: Sketch the pole-zero plot for H(s) = (s+2)/((s+1)(s+3)). Is it stable? What type of filter is it? |

**Self-test:** Where must poles be for a stable causal continuous-time system? What does each component of a Bode plot show?

---

### 📅 Day 7 — Sunday, June 14
**Topic: Z-Transform — The Bridge to Digital**

| Time | Activity |
|---|---|
| 0:00–0:50 | Re-read **Lecture 9** (dsp09.pdf) in full — z-transform definition, ROC, relationship to DTFT, common z-transform pairs |
| 0:50–1:20 | Re-read **Lecture 10** (dsp10.pdf) — z-transform properties, inverse z-transform, transfer functions in z-domain |
| 1:20–1:50 | Re-run **Lab 09** — z-plane exercises, stability analysis. Work through the H(z) = 1/(z-0.5) example carefully |
| 1:50–2:00 | Review **hw9** — you only answered 1 question. Read the full hw9 assignment (dsp_homework09.pdf) and attempt the remaining questions |

> [!IMPORTANT]
> This is where your gaps begin. Pay extra attention from here onwards.

**Self-test:** Where must poles be for a stable causal discrete-time system? What is the ROC for a causal system?

---

### 📅 Day 8 — Monday, June 15
**Topic: Digital Filter Fundamentals (FIR vs IIR)**

| Time | Activity |
|---|---|
| 0:00–0:50 | Re-read **Lecture 10** (dsp10.pdf) — FIR vs IIR filters, difference equations, impulse response |
| 0:50–1:20 | Re-read **Lecture 11** (dsp11.pdf) — filter design basics, frequency response from H(z) |
| 1:20–1:50 | Re-run **Lab 10** — impulse response of LTI systems, `plot_zplane.py` utility |
| 1:50–2:00 | Read the **hw10** assignment (dsp_homework10.pdf) and attempt at least the first 2–3 questions |

**Self-test:** What is the key difference between FIR and IIR filters? Why are IIR filters potentially unstable? Write the general difference equation.

---

### 📅 Day 9 — Tuesday, June 16
**Topic: Notch Filters & Filter Specifications**

| Time | Activity |
|---|---|
| 0:00–0:50 | Re-read **Lecture 11** (dsp11.pdf) — notch filter theory, pole-zero placement for targeted frequency removal |
| 0:50–1:20 | Re-run **Lab 11** — manually design a 2nd-order notch filter (f₀=20 Hz, Δf=4 Hz, fs=160 Hz). This lab walks you through it step by step |
| 1:20–1:50 | Read **hw11** assignment (dsp_homework11.pdf) and attempt the exercises |
| 1:50–2:00 | Summarise: How do you place poles and zeros to create a notch? Why must poles be inside the unit circle? |

**Self-test:** Design a notch filter for 50 Hz hum removal at fs=500 Hz. Where do you place the zeros? Where do the poles go?

---

## Phase 2: Deep Study (8 hours/day)

---

### 📅 Day 10 — Wednesday, June 17
**Topic: Deep dive — Convolution, FT & Sampling (Lectures 1–5)**

| Time | Activity |
|---|---|
| 0:00–1:30 | **Theory review:** Re-read Lectures 1–3 in detail. Take handwritten notes of all key formulas |
| 1:30–2:30 | **Problem solving:** Redo hw1, hw2, hw3 from scratch without looking at your old solutions |
| 2:30–3:00 | ☕ Break |
| 3:00–4:30 | **Theory review:** Re-read Lectures 4–5. Focus on all FT properties and the complete sampling pipeline |
| 4:30–5:30 | **Problem solving:** Redo hw4, hw5 from scratch. Can you derive the aliasing formula? |
| 5:30–6:00 | ☕ Break |
| 6:00–7:00 | **Lab practice:** Re-run Labs 02–05. Modify parameters, experiment, understand what happens |
| 7:00–8:00 | **Self-testing:** Create flashcards for all formulas from today. Test yourself on 10 sample problems |

---

### 📅 Day 11 — Thursday, June 18
**Topic: Deep dive — DFT, FFT, PSD & Welch (Lectures 6–7)**

| Time | Activity |
|---|---|
| 0:00–1:30 | **Theory review:** Re-read Lectures 6–7 thoroughly. Write down every formula: DFT, inverse DFT, frequency resolution, Welch steps |
| 1:30–2:30 | **Problem solving:** Redo hw6, hw7 completely. Fill in the gaps in hw7 (especially question 7 about variance reduction) |
| 2:30–3:00 | ☕ Break |
| 3:00–4:30 | **Lab deep dive:** Work through Lab 06 (FFT) and Lab 07 (Welch PSD) step by step. Modify the code to use different window sizes and overlap ratios. Observe how the PSD changes |
| 4:30–5:30 | **Practical application:** Look at your mofette project code (`dsp_analysis.py`). You already implemented Welch PSD and spectrograms — review that code as applied examples |
| 5:30–6:00 | ☕ Break |
| 6:00–7:00 | **Window functions deep dive:** Compare rectangular, Hann, Hamming, Blackman windows. Understand main lobe width vs. side lobe attenuation tradeoff |
| 7:00–8:00 | **Practice problems:** Compute DFT by hand for a 4-point signal. Calculate frequency bins and resolution for given parameters |

---

### 📅 Day 12 — Friday, June 19
**Topic: Deep dive — Laplace & Z-Transform (Lectures 8–10) ⚠️ CRITICAL**

| Time | Activity |
|---|---|
| 0:00–1:30 | **Theory review:** Re-read Lectures 8–9. Map out the parallels between s-domain and z-domain systematically |
| 1:30–2:30 | **Problem solving:** Redo hw8 completely. Then work through **hw9** — solve ALL assigned questions (you only did 1!) |
| 2:30–3:00 | ☕ Break |
| 3:00–4:30 | **Z-transform deep dive:** Re-read Lecture 10. Practice: z-transform pairs, inverse z-transform, ROC determination. Work through **hw10** (dsp_homework10.pdf) — this is one you never attempted |
| 4:30–5:30 | **Lab practice:** Work through Lab 09 (z-plane stability) and Lab 10 (impulse response). Use `plot_zplane.py` to visualise pole-zero configurations |
| 5:30–6:00 | ☕ Break |
| 6:00–7:30 | **Stability analysis practice:** For 10 different transfer functions H(z), determine: poles, zeros, ROC, stability, causality, filter type. Draw pole-zero plots by hand |
| 7:30–8:00 | **Formula sheet:** Create a comprehensive s-domain ↔ z-domain comparison table |

> [!CAUTION]
> This is your weakest area. If you feel shaky after today, plan to revisit z-transform exercises on Day 14 or 15.

---

### 📅 Day 13 — Saturday, June 20
**Topic: Deep dive — Digital Filter Design (Lectures 11–12) ⚠️ CRITICAL**

| Time | Activity |
|---|---|
| 0:00–1:30 | **Theory review:** Re-read Lectures 11–12. Focus on: notch filter pole-zero placement, Butterworth design, bilinear transform, frequency warping |
| 1:30–2:30 | **Problem solving:** Work through **hw11** (dsp_homework11.pdf) — notch filter design exercises (never attempted!) |
| 2:30–3:00 | ☕ Break |
| 3:00–4:30 | **Lab deep dive:** Work through Lab 11 (manual notch filter: 40 dB attenuation at 20 Hz, Δf=4 Hz). Understand every step of the design process |
| 4:30–5:30 | **Problem solving:** Work through **hw12** (dsp_homework12.pdf) — classical filter design (never attempted!) |
| 5:30–6:00 | ☕ Break |
| 6:00–7:30 | **Lab deep dive:** Work through Lab 12 (classical digitised filters — Butterworth, Chebyshev, audio filtering). Apply filters to the provided audio file. Compare filter types |
| 7:30–8:00 | **Practical connection:** Review your mofette project's `dsp_analysis.py` — you used `butter()` and `sosfiltfilt()` for lowpass and bandpass filtering. Connect this to the theory |

---

### 📅 Day 14 — Sunday, June 21
**Topic: Wavelets + Comprehensive Review of Weak Areas**

| Time | Activity |
|---|---|
| 0:00–1:00 | **Theory review:** Read Lecture 13 (dsp13.pdf) — continuous wavelets, CWT, scalograms |
| 1:00–1:30 | **Lab practice:** Work through Lab 13 — continuous wavelet exercises |
| 1:30–2:00 | ☕ Break |
| 2:00–4:00 | **🔁 Revisit Z-transform & digital filters:** Redo the hardest problems from hw10, hw11, hw12. Focus on any concepts that felt shaky on Days 12–13 |
| 4:00–4:30 | ☕ Break |
| 4:30–6:00 | **Cross-topic connections:** Create a "big picture" diagram connecting: Time domain → Frequency domain → s-domain → z-domain → Filter implementation. Understand how each transformation relates to the others |
| 6:00–6:30 | ☕ Break |
| 6:30–8:00 | **Create your formula sheet:** Write a comprehensive 2-page formula reference covering all 13 lectures. This should include every key equation, condition, and definition |

---

### 📅 Day 15 — Monday, June 22
**Topic: Full Mock Exam & Final Review**

| Time | Activity |
|---|---|
| 0:00–2:00 | **Mock exam:** Go through ALL 12 homework PDFs as if they were exam questions. Time yourself — attempt each one without notes |
| 2:00–2:30 | ☕ Break |
| 2:30–4:00 | **Grade yourself:** Check your mock exam answers against your old solutions and the lecture material. Identify any remaining gaps |
| 4:00–4:30 | ☕ Break |
| 4:30–6:00 | **Targeted gap filling:** Spend this block exclusively on the topics you got wrong in the mock exam. Re-read the relevant lecture sections |
| 6:00–6:30 | ☕ Break |
| 6:30–7:30 | **Final formula review:** Go through your formula sheet one last time. Test yourself: cover the right side and try to recall each formula |
| 7:30–8:00 | **Confidence check:** List 3 things you're most confident about and 3 things you're least confident about. Do a final 15-minute drill on the weak items |

---

### 📅 Day 16 — Tuesday, June 23 🎯 EXAM DAY

| Time | Activity |
|---|---|
| Morning | Light review of your formula sheet (30 min max). **Do not cram.** |
| Before exam | Eat well, stay hydrated, arrive early |
| During exam | Read all questions first. Start with what you know best. Budget time per question |

---

## 📋 Key Formulas to Memorise

These appear across multiple lectures and are nearly guaranteed on any DSP exam:

| Formula | Context |
|---|---|
| `y[n] = Σ x[k]·h[n-k]` | Discrete convolution |
| `X(f) = ∫ x(t)·e^{-j2πft} dt` | Continuous Fourier Transform |
| `X[k] = Σ x[n]·e^{-j2πkn/N}` | Discrete Fourier Transform |
| `Δf = fs / N = 1 / T` | Frequency resolution |
| `fs ≥ 2·fmax` | Nyquist criterion |
| `f_alias = |f - round(f/fs)·fs|` | Alias frequency |
| `X(z) = Σ x[n]·z^{-n}` | Z-transform |
| `H(z) = Y(z) / X(z)` | Transfer function (discrete) |
| `H(s) = N(s) / D(s)` | Transfer function (continuous) |
| Stable causal DT system: all poles inside unit circle | Z-domain stability |
| Stable causal CT system: all poles in left half-plane | S-domain stability |

---

## 📊 Time Budget Summary

| Phase | Days | Hours/day | Total hours |
|---|---|---|---|
| Phase 1 (review) | Jun 8–16 (9 days) | 2 h | **18 h** |
| Phase 2 (deep study) | Jun 17–22 (6 days) | 8 h | **48 h** |
| Exam day warm-up | Jun 23 | 0.5 h | **0.5 h** |
| **Total** | **16 days** | | **~66.5 h** |

> [!TIP]
> Your mofette project code is an excellent practical reference — you've already implemented Welch PSD, Butterworth filters, spectrograms, and cross-correlation. When reviewing those topics in theory, open `dsp_analysis.py` side by side. Real-world application reinforces learning.

Good luck! 🍀
