import matplotlib.pyplot as plt
import numpy as np

T = 0.001
fs = 1 / T
fmax = 0.8 * fs / 2

N = 4096
f = np.fft.fftfreq(N, T)

X = np.zeros(N)
X[abs(f) <= fmax] = (1 - abs(f/fmax))[abs(f) <= fmax]

# plt.plot(np.fft.fftshift(f), np.fft.fftshift(X), '-')

x = fs * np.real(np.fft.ifft(X))

t = np.fft.fftfreq(N, fs/N)

# plt.plot(np.fft.fftshift(t), np.fft.fftshift(x))

X1 = T * np.fft.fft(x)

# plt.plot(np.fft.fftshift(f), np.fft.fftshift(X1), '.')

m = 16
dt = T * m

xhat = x[::m]

tsamp = t[::m]

# plt.plot(np.fft.fftshift(tsamp), np.fft.fftshift(xhat), 'o')

def sincpi(x):
    x [x == 0] = 1e-13
    return np.sin(np.pi * x) / (np.pi * x)

# plt.plot(np.fft.fftshift(t), np.fft.fftshift(sincpi(t/dt)))

Nsamp = int(N // m)

xrec = np.zeros(len(t))

for n in np.arange(-Nsamp // 2, Nsamp // 2):
    xrec += xhat[n] * sincpi(t/dt - n)

# plt.plot(np.fft.fftshift(t), np.fft.fftshift(xrec))
plt.plot(np.fft.fftshift(t), np.fft.fftshift(x))

plt.show()