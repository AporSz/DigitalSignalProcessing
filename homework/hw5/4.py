import numpy as np
import matplotlib.pyplot as plt

from numpy.fft import fft, ifft, fftshift, ifftshift, fftfreq

dt = 0.001
fs = 1/dt

# fmax > 0
fmax = 4
N = 4096

f = fftfreq(N, dt)

X = np.zeros(N)
X[abs(f) < fmax]  = (fmax ** 2 - f ** 2)[abs(f) < fmax]

# a
plt.plot(fftshift(f), fftshift(X))
plt.xlim(-10, 10)
plt.show()

x = fs * np.real(ifft(X))

t = fftfreq(N, fs/N)

# b
plt.plot(fftshift(t), fftshift(x))
plt.show()

m = 16
T = dt * m
xhat = x[::m]
tsamp = t[::m]

# c
plt.plot(fftshift(t), fftshift(x))
plt.plot(fftshift(tsamp), fftshift(xhat), '.')
plt.show()


# d
fsamp = fftfreq(N // m, dt * m)

plt.plot(fftshift(fsamp), np.real(fftshift(fft(xhat))) / fs * m, '.')
plt.plot(fftshift(f), fftshift(X))
plt.xlim(-10, 10)

plt.show()

Nsamp = N//m # size of the sampled signal (the same as len(xhat))
xrec = np.zeros(len(t)) # the reconstructed signal ('continuous')
for n in np.arange(-Nsamp//2, Nsamp//2):
    xrec += xhat[n]*np.sinc(t/T - n)

plt.plot(fftshift(t), fftshift(x))
plt.plot(fftshift(t), fftshift(xrec), '.')

plt.show()