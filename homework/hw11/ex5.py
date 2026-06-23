from scipy import signal

import numpy as np
import matplotlib.pyplot as plt

num_taps = 51
cutoff_freq = 0.3
h = signal.firwin(num_taps, cutoff_freq, window='hamming')

w, h_freq = signal.freqz(h, worN=1024)

normalized_freq = w / np.pi
mag_db = 20 * np.log10(np.abs(h_freq))
phase = np.angle(h_freq, deg = True)

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

ax1.plot(normalized_freq, mag_db, label = "Magnitude")
ax1.grid()
ax1.legend()

ax2.plot(normalized_freq, phase, label = "Phase")
ax2.grid()
ax2.legend()

plt.show()
