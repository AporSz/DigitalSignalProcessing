from scipy import signal

import numpy as np
import matplotlib.pyplot as plt

fs = 8000
fc = 1000

b, a = signal.butter(1, 2 * np.pi * fc, btype='lowpass', analog=True)

bz, az = signal.bilinear(b, a, fs=fs)

w, h = signal.freqs(b, a)
wz, hz = signal.freqz(bz, az, fs=fs)

plt.plot(w/(2 * np.pi), np.abs(h))
plt.plot(wz, np.abs(hz), 'k--')

plt.show()

plt.plot(w/(2 * np.pi), np.angle(h))
plt.plot(wz, np.angle(hz), 'k--')

plt.show()

b, a = signal.butter(1, 2 * fs * np.tan(np.pi * fc / fs), btype='lowpass', analog=True)

bz, az = signal.bilinear(b, a, fs=fs)

w, h = signal.freqs(b, a)
wz, hz = signal.freqz(bz, az, fs=fs)

plt.plot(w/(2 * np.pi), np.abs(h))
plt.plot(wz, np.abs(hz), 'k--')

plt.show()

plt.plot(w/(2 * np.pi), np.angle(h))
plt.plot(wz, np.angle(hz), 'k--')

plt.show()