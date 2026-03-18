# DSP 1 – Theory

## 1(a) Ways to classify a signal:
* **Time:** Continuous-time vs. Discrete-time
* **Amplitude:** Continuous-amplitude vs. Discrete-amplitude
* **Predictability:** Deterministic (exact formula) vs. Random (probabilities)
* **Repetition:** Periodic (repeats) vs. Aperiodic (no pattern)

## 1(b) Mathematical vs. Physical representation:
* **Physical:** The actual real-world phenomenon (e.g., voltage in a wire, soundwaves).
* **Mathematical:** The abstract equation used to model it on paper (e.g., `x(t) = cos(t)`).

## 1(c) Continuous-time, discrete-time, and digital signals:
* **Continuous-time:** Smooth, unbroken time and amplitude. 
  * *Math:* `x(t)`
* **Discrete-time:** Time is sliced into specific steps (sampled), but amplitude can be any exact value. 
  * *Math:* `x[n]`
* **Digital:** Both time and amplitude are restricted to specific steps (sampled and quantized). It's what computers use.

## 1(d) Concept of a system and mathematical representation:
* **Concept:** A process or device that takes an input signal, modifies it, and spits out an output signal.
* **Math:** An operator (like `T`) mapping input to output. 
  * *Example:* `y[n] = T{x[n]}`

## 1(e) Continuous-time vs. Discrete-time systems + examples:
* **Continuous-time system:** Takes continuous inputs, gives continuous outputs. 
  * *Example:* An analog guitar pedal or audio amplifier.
* **Discrete-time system:** Takes discrete inputs, gives discrete outputs. 
  * *Example:* A software algorithm calculating a moving average.

## 1(f) Is a continuous-time system an analog system?
* **Yes.** In practical engineering, the terms are used interchangeably because real-world continuous-time systems (like electrical circuits) also have continuous amplitudes.

## 1(g) Why and where do we need interface systems?
* **Why:** To act as a translator. The real world is continuous (analog), but computers only understand discrete math (digital).
* **Where:** At the boundaries of any digital processing system—connecting the physical sensors/microphones to the computer, and the computer back to physical actuators/speakers.
* **Block Diagram:** `Analog Signal -> [ A/D Converter ] -> Digital Processor -> [ D/A Converter ] -> Analog Signal`

## 1(h) Describe an analog-to-digital (A/D) converter:
* **What it does:** Converts a continuous-time, continuous-amplitude analog signal into a discrete digital signal made of binary numbers.
* **The 3 Steps:**
  1. **Sampling:** Takes snapshots of the signal at specific time intervals.
  2. **Quantization:** Rounds the exact amplitude of that snapshot to the nearest available fixed level.
  3. **Coding:** Turns that rounded level into a binary number (1s and 0s).

## 1(i) Describe a digital-to-analog (D/A) converter:
* **What it does:** The exact opposite of an A/D converter. It takes a stream of discrete digital numbers and reconstructs a continuous analog waveform.
* **How:** It takes the digital values and usually holds them to create a "staircase" voltage, which is then passed through a smoothing filter (low-pass filter) to recreate a fluid, continuous curve.

## 1(j) Practical vs. Ideal Converters:
* **Ideal vs. Practical A/D:** An ideal A/D converter happens instantly and has infinite precision (no rounding errors). A practical A/D introduces "quantization noise" (the error from rounding), has a limited voltage range (it can "clip" if the signal is too loud), and has a slight processing delay.
* **Ideal vs. Practical D/A:** An ideal D/A instantly reconstructs the perfect original analog signal. A practical D/A outputs a slightly distorted signal that requires physical smoothing filters, has limited resolution, and introduces slight electronic noise.

## 1(k) What is signal processing and its forms?
* **What it is:** The mathematical or physical manipulation of a signal to extract information, remove noise, or change its format.
* **Forms & Examples:** 1. **Analog Signal Processing (ASP):** Modifying physical waveforms. *Example:* A traditional FM radio tuner or a vinyl record player's amplifier. 
  2. **Digital Signal Processing (DSP):** Modifying streams of numbers. *Example:* MP3 audio compression or a smartphone camera applying a photo filter.

## 1(l) Describe Analog Signal Processing (ASP):
* **Description:** Processing continuous physical signals directly using electronic components like resistors, capacitors, and op-amps.
* **Simplified Block Diagram:** `Analog Input Signal -> [ Analog Processor ] -> Analog Output Signal`

## 1(m) Describe Digital Signal Processing (DSP):
* **Description:** Processing signals as sequences of discrete numbers using computers, microprocessors, or specialized DSP chips.
* **Simplified Block Diagram:** `Analog Input -> [ A/D Converter ] -> [ Digital Processor ] -> [ D/A Converter ] -> Analog Output`

## 1(n) Why is DSP preferred over ASP? Are there disadvantages?
* **Why it's preferred (Advantages):** * **Perfect Reproducibility:** It relies on math, not physical parts, so it is immune to temperature changes, component aging, or manufacturing tolerances.
  * **Flexibility:** You can completely change the system just by updating the software code, without rewiring hardware.
  * **Complexity:** Can perform highly complex mathematical operations that are impossible to build with physical analog circuits.
* **Disadvantages:**
  * **Hardware Overhead:** Always requires extra A/D and D/A converters.
  * **Speed Limits:** ASP can sometimes handle extremely high-frequency signals (like microwaves) faster and cheaper than the massive computing power required to sample them digitally.
  * **Power Consumption:** Continuously running a microprocessor can use more power than a simple passive analog circuit.

## Question 2: Data Generation and File I/O
**Objective:** Generate an array, calculate its sine, and write the data to both text and binary files without using explicit loops.

```python
import numpy as np

# 2(a) Generate an array from 0.5 to 10 with a step of 0.5 
# Note: The stop value in arange is exclusive, so we use 10.5 to include 10.
x = np.arange(0.5, 10.5, 0.5)

# 2(b) Write to a text file in two columns
y = np.sin(x)
data_columns = np.column_stack((x, y))
np.savetxt('sine_data.txt', data_columns, fmt='%.4f', delimiter='\t', header='x\tsin(x)')

# 2(c) Write to a binary file in 32-bit float format 
data_32bit = data_columns.astype(np.float32)
data_32bit.tofile('sine_data.bin')
print("Data successfully saved to 'sine_data.txt' and 'sine_data.bin'.")
```

## Question 3: Reading Data and Plotting

**Objective:** Write a Python script without using loops that reads the previously written array from the binary file, plots the sine curve with labeled axes, a grid, a legend, and a title, and saves the figure.

```python
import numpy as np
import matplotlib.pyplot as plt

# 3(a) Read in the previously written array from the binary file
read_data = np.fromfile('sine_data.bin', dtype=np.float32)
read_data = read_data.reshape(-1, 2)

x_read = read_data[:, 0]
y_read = read_data[:, 1]

# 3(b) Plot the sine curve with all required formatting
plt.figure(figsize=(8, 5))
plt.plot(x_read, y_read, marker='o', linestyle='-', color='b', label='sin(x)')

plt.xlabel('x values')
plt.ylabel('Amplitude')
plt.title('Sine Wave Generated from Binary Data')
plt.grid(True)
plt.legend()

# 3(c) Save the figure to your local directory
plt.savefig('sine_plot.png', dpi=300, bbox_inches='tight')
print("Plot successfully generated and saved as 'sine_plot.png'.")
```
# DSP Homework - Question 4: Formal System Property Proofs

## 4(a) y[n] = cos(x[n]) + n
1. Linearity: Non-Linear
Proof: Let x3[n] = a * x1[n] + b * x2[n]. 
The system response to x3[n] is:
y3[n] = cos(a * x1[n] + b * x2[n]) + n

The scaled sum of the individual responses is:
a * y1[n] + b * y2[n] = a * (cos(x1[n]) + n) + b * (cos(x2[n]) + n)

Since y3[n] is NOT EQUAL to a * y1[n] + b * y2[n], the system is non-linear.

2. Time-Invariance: Time-Variant
Proof: Let the input be delayed by k samples: x2[n] = x1[n-k].
The system response to the delayed input is:
y2[n] = cos(x1[n-k]) + n

Now, delay the original output by k samples:
y1[n-k] = cos(x1[n-k]) + (n - k)

Since y2[n] is NOT EQUAL to y1[n-k], the system is time-variant.

3. Causality: Causal
Reasoning: The output y[n] depends only on the input at the current time index n (specifically x[n]). It does not require any future values like x[n+1].

4. Memory: Memoryless
Reasoning: The system only evaluates the input at the exact moment n. It does not store or use past values like x[n-1].

---

## 4(b) y[n] = (2^-n) * x[n]
1. Linearity: Linear
Proof: Let x3[n] = a * x1[n] + b * x2[n].
y3[n] = (2^-n) * (a * x1[n] + b * x2[n])
y3[n] = a * ((2^-n) * x1[n]) + b * ((2^-n) * x2[n])
y3[n] = a * y1[n] + b * y2[n]
Because superposition holds, the system is linear.

2. Time-Invariance: Time-Variant
Proof: Delay the input by k: x2[n] = x1[n-k].
y2[n] = (2^-n) * x1[n-k]

Delay the output by k:
y1[n-k] = (2^-(n-k)) * x1[n-k]

Since 2^-n is NOT EQUAL to 2^-(n-k), the outputs don't match (y2[n] != y1[n-k]). The system is time-variant.

3. Causality: Causal
Reasoning: Depends only on the current input x[n].

4. Memory: Memoryless
Reasoning: Evaluates only at the present index n.

---

## 4(c) y[n] = sum of x[n-k] from k=0 to 9 
(Note: Assuming the garbled text refers to a standard 10-point moving sum)

1. Linearity: Linear
Reasoning: The system is a finite sum of scaled inputs. The sum operator is inherently linear: the sum of (a*x1 + b*x2) is equal to a*(sum of x1) + b*(sum of x2).

2. Time-Invariance: Time-Invariant
Reasoning: A shift in the input by m samples results in the sum of x[(n-m)-k], which is exactly identical to shifting the final output y[n] by m.

3. Causality: Causal
Reasoning: The index is n-k where k >= 0. Therefore, it only accesses present (n) and past (n-1, n-2...) values.

4. Memory: Has Memory
Reasoning: It explicitly requires past values of the input (up to x[n-9]) to compute the current output.

---

## 4(d) y[n] = x[n] / (1 + |x[n]|)
1. Linearity: Non-Linear
Proof: We can prove this by showing it fails the scaling property. 
Let x1[n] = 1. The output is y1[n] = 1 / (1 + 1) = 0.5.
Now, let's scale the input by a factor of 2: x2[n] = 2 * x1[n] = 2.
The new output is y2[n] = 2 / (1 + 2) = 2/3 (which is roughly 0.667).
If the system were linear, y2[n] should equal 2 * y1[n], which would be 2 * 0.5 = 1. 
Since 2/3 is NOT EQUAL to 1, the system is non-linear.

2. Time-Invariance: Time-Invariant
Reasoning: Delaying the input by k makes the output x[n-k] / (1 + |x[n-k]|), which is exactly equal to delaying the output y[n-k]. There are no standalone "n" variables outside the input.

3. Causality: Causal
Reasoning: The output only depends on the present input x[n].

4. Memory: Memoryless
Reasoning: It only evaluates the input at the exact moment n.

---

## 4(e) y[n] = (x[n])^3
1. Linearity: Non-Linear
Proof: Let x3[n] = a * x1[n]. 
The system response is y3[n] = (a * x1[n])^3 = (a^3) * (x1[n]^3).
For the system to be linear, the output must be a * y1[n] = a * (x1[n]^3).
Since (a^3) * (x1[n]^3) is NOT EQUAL to a * (x1[n]^3) for all values of a (except 0, 1, -1), it fails the scaling property and is non-linear.

2. Time-Invariance: Time-Invariant
Reasoning: Delaying the input by k results in (x[n-k])^3. This perfectly matches the delayed output y[n-k].

3. Causality: Causal
Reasoning: Only depends on the current input x[n].

4. Memory: Memoryless
Reasoning: Only relies on the present moment n.

---

## 4(f) y[n] = x[n] - x[n-1] + 0.5 * y[n-1]
1. Linearity: Linear
Reasoning: This is a Linear Constant-Coefficient Difference Equation. Since all terms involving x and y are strictly to the first power and there are no standalone constants added, it satisfies superposition.

2. Time-Invariance: Time-Invariant
Reasoning: The coefficients (1, -1, and 0.5) are constant and do not depend on the time index n.

3. Causality: Causal
Reasoning: To find y[n], you only need x[n], x[n-1], and y[n-1]. No future values (like x[n+1]) are required.

4. Memory: Has Memory
Reasoning: It relies heavily on memory to store both the previous input x[n-1] and the previous output state y[n-1].

---

## 4(g) y[n] = 1 if |x[n]| <= 1, otherwise 0
1. Linearity: Non-Linear
Proof: This system acts as a hard threshold, which easily fails scaling.
Let x1[n] = 1. Since |1| <= 1, the output y1[n] = 1.
Now, let's scale the input by 2: x2[n] = 2 * x1[n] = 2. 
Since |2| is NOT <= 1, the new output is y2[n] = 0.
If it were linear, y2[n] should be 2 * y1[n] = 2 * 1 = 2. 
Since 0 is NOT EQUAL to 2, the system is non-linear.

2. Time-Invariance: Time-Invariant
Reasoning: The conditional rule does not change depending on what the time index "n" is. Delaying the input yields the exact same delayed output.

3. Causality: Causal
Reasoning: The condition is only checked against the current input x[n].

4. Memory: Memoryless
Reasoning: It only needs to look at the value at the exact moment n to make its decision.

---

## 4(h) y[n] = e^(x[n]) - 1
1. Linearity: Non-Linear
Proof: Let x3[n] = a * x1[n] + b * x2[n].
y3[n] = e^(a * x1[n] + b * x2[n]) - 1
This is NOT EQUAL to a * (e^(x1[n]) - 1) + b * (e^(x2[n]) - 1). The exponential operator destroys linearity.

2. Time-Invariance: Time-Invariant
Reasoning: Delaying the input by k makes the output e^(x1[n-k]) - 1, which is exactly equal to delaying the output y1[n-k].

3. Causality: Causal
Reasoning: Only evaluates the current index n.

4. Memory: Memoryless
Reasoning: Only requires the input at the exact present moment n.
