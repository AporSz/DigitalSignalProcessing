import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq, fftshift

# --- 1. Create a short time-domain signal ---
fs = 100.0           # Sampling rate (100 Hz)
N = 64               # Original number of samples
t = np.arange(N) / fs

# We choose 10.5 Hz. With N=64 and fs=100, the natural FFT bins are at
# multiples of 1.5625 Hz (0, 1.56, 3.12... 9.375, 10.93...).
# 10.5 Hz falls directly between bins!
y = np.sin(2 * np.pi * 10.5 * t)

# --- 2. Unpadded FFT (The raw, blocky data) ---
# Calculate positive frequencies only
f_unpadded = fftfreq(N, 1/fs)
Y_unpadded = np.abs(fft(y)) / N # Normalized magnitude

# --- 3. Zero-Padded FFT (The smooth interpolation) ---
N_padded = 512 # Pad out to 512 points (adding 448 zeros)

# NumPy's fft function automatically zero-pads if you pass a length (n)
# that is larger than your input array!
f_padded = fftfreq(N_padded, 1/fs)
Y_padded = np.abs(fft(y, n=N_padded)) / N


# Plot the raw, unpadded FFT as blue dots
plt.plot(fftshift(f_unpadded), fftshift(Y_unpadded), 'o')

# Plot the padded FFT as a smooth orange line
plt.plot(fftshift(f_padded), fftshift(Y_padded), '.-')

plt.show()