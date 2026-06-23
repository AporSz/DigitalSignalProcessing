from scipy import signal

import numpy as np
import matplotlib.pyplot as plt

fs = 160
f0 = 20
bw = 4

w0 = 2 * np.pi * f0/fs
r = 1 - (2 * np.pi * (bw/fs)) / 2

K = (1 - 2 * r * np.cos(w0) + r ** 2) / (2 - 2 * np.cos(w0))

num = [K, -2 * K * np.cos(w0), K]
denom = [-1, -2 * r * np.cos(w0), r ** 2]

w, h = signal.freqz(num, denom, worN=1024, fs=fs)

mag_db = 20 * np.log10(np.abs(h))
phase_deg = np.angle(h, deg=True)

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

ax1.plot(w, mag_db, label = "Magnitude")
ax1.axhline(-40, color = 'black', linestyle = '--', label = "-40 dB")
ax1.axvline(f0, color = 'grey', linestyle = ':', label = "20 Hz")
ax1.grid()
ax1.legend()

ax2.plot(w, phase_deg, label = "Phase")
ax2.axvline(f0, color = 'black', linestyle = '--', label = "20 Hz")
ax2.grid()
ax2.legend()

plt.show()
