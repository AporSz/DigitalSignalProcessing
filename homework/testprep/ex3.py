from scipy import signal

import numpy as np
import matplotlib.pyplot as plt

fs = 10000

b, a = signal.butter(3, [1000 * np.pi * 2, 3000 * np.pi * 2], btype='bandpass', analog=True)

bz, az = signal.bilinear(b, a, fs=fs)

bpre, apre = signal.butter(3, [2 * fs * np.tan(np.pi * 1000/fs), 2 * fs * np.tan(np.pi * 3000/fs)], btype='bandpass', analog=True)

bprez, aprez = signal.bilinear(bpre, apre, fs=fs)

wz, hz = signal.freqz(bz, az, fs=fs)
w, h = signal.freqs(b, a)

wpre, hpre = signal.freqs(b, a)
wprez, hprez = signal.freqz(bprez, aprez, fs=fs)

plt.plot(w / (np.pi * 2), np.abs(h), linewidth=5, alpha=0.5)
plt.plot(wz, np.abs(hz), 'k--')

plt.show()

plt.plot(wpre / (np.pi  *2), np.abs(hpre), linewidth=5, alpha=0.5)
plt.plot(wprez, np.abs(hprez), 'k--')

plt.show()
