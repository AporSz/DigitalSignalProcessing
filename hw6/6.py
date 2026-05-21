import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq, fftshift

# --- 1. Setup the Time Domain ---
fs = 100.0  # Sampling frequency (100 Hz)
N = 100     # Number of samples (100 points)
t = np.arange(N) / fs

# With fs=100 and N=100, our FFT bins are exactly at integers: 0, 1, 2, 3... Hz

# --- 2. Create the Signals ---
# Case 1: Perfectly aligns with an FFT bin
f_on = 10.0
y_on = np.cos(2 * np.pi * f_on * t)

# Case 2: Falls exactly halfway between the 10Hz and 11Hz bins
f_off = 10.5
y_off = np.cos(2 * np.pi * f_off * t)

# --- 3. Compute FFTs ---
# Get positive frequencies only, normalize by N/2 to get true amplitude of 1.0
freqs = fftshift(fftfreq(N, 1/fs))
Y_on = fftshift(np.abs(fft(y_on)) / N)
Y_off = fftshift(np.abs(fft(y_off)) / N)

# --- 4. Plotting ---
plt.figure(figsize=(10, 6))

# Plot On-Bin (Blue)
plt.plot(freqs, Y_on, 'o-')

# Plot Off-Bin (Orange)
plt.plot(freqs, Y_off, 's-')

# Zoom in around the peaks
# plt.xlim(5, 15)

plt.show()