from scipy import signal
from pywt import *
from numpy.fft import *

import numpy as np
import matplotlib.pyplot as plt

T = 20

fs = 500
dt = 1/fs

t = np.arange(0, T, dt)
N = len(t)

f = np.zeros_like(t)
f[t < 10] += np.sin(2 * np.pi * 50 * t)[t < 10]
f[t >= 5] += np.sin(2 * np.pi * 100 * t)[t >= 5]

plt.plot(t, f)
plt.xlim([4.75, 5.25])

plt.show()

freq, time, Sxx = signal.spectrogram(f, fs=fs)

plt.pcolormesh(time, freq, Sxx)
plt.show()

frequencies = np.arange(1, 110)
wavelet = 'cmor15.5-1.0'

scales = central_frequency(wavelet) * fs / frequencies
coef, freq_out = cwt(f, scales, wavelet, sampling_period=dt)

Z = np.abs(coef)

plt.pcolormesh(t, freq_out, Z)
plt.show()

b, a = signal.butter(3, [25, 75], btype='bandpass', fs=fs)

ffiltered = signal.filtfilt(b, a, f)
freqf, timef, Sxxf = signal.spectrogram(ffiltered, fs=fs)

plt.pcolormesh(timef, freqf, Sxxf)
plt.show()

freqpsd, psd = signal.welch(f, fs=fs)
freqfiltered, psdfiltered = signal.welch(ffiltered, fs=fs)
plt.plot(freqpsd, psd)
plt.plot(freqfiltered, psdfiltered, 'k--')
plt.show()
