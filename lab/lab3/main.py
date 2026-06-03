import numpy as np
import matplotlib.pyplot as plt

x = np.array([0, 1, 2, 3, 4, 3, 2, 1])

np.fft.fft(x)

N = 8
dt = 0.1

f = np.fft.fftfreq(N, dt)

np.fft.fftshift(f)

np.fft.fftshift(x)

t = np.arange(-10, 10, 0.01)

x = np.exp(-t*t)

# t = np.linspace(-10, 10, 2**10)

X = np.fft.fft(x)
f = np.fft.fftfreq(len(t), dt)

plt.plot(f, abs(X), '.-')
plt.plot(f, x, '.-')

x = np.exp(-t*t/0.1)

X = np.fft.fft(x)
f = np.fft.fftfreq(len(t), dt)

plt.plot(f, abs(X), '.-')
plt.plot(f, x, '.-')

plt.show()