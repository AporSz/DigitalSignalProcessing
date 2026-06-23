import numpy as np
import matplotlib.pyplot as plt
from optype.numpy.compat import signedinteger
import pywt

from scipy import signal
import matplotlib

plt.style.use('dark_background')
#matplotlib.use('TkAgg')

f = np.fromfile("eeg.bin", dtype=np.float32)

plt.plot(f)
plt.show()

fs = 200

freq, times, Sxx = signal.spectrogram(f, fs, nperseg=1024)
plt.pcolormesh(times, freq, 10 * np.log10(Sxx))
plt.show()

chunk = f[0:10 * fs]
chunk = chunk - chunk.mean()
wavelet = 'cmor15.5-1.0'
frequencies = np.arange(1, 50, 0.5)
scales = pywt.central_frequency(wavelet) * fs / frequencies

coef, freq_out = pywt.cwt(chunk, scales, wavelet, sampling_period=1/fs, method='fft')

time = np.linspace(0, 10, len(chunk))
Z = np.abs(coef)

plt.pcolormesh(time, freq_out, Z)
plt.show()

b, a = signal.butter(3, [10, 20], btype='bandpass', fs=fs)

filtered = signal.filtfilt(b, a, f)

freqs, psd = signal.welch(f, fs)
filt_freqs, filt_psd = signal.welch(filtered, fs)

plt.semilogy(freqs, psd, linewidth=3, alpha=0.7)
plt.semilogy(filt_freqs, filt_psd, linewidth=1)

plt.show()

freqs, times, Sxx = signal.spectrogram(filtered, fs)
plt.pcolormesh(times, freqs, Sxx)
plt.show()
