import numpy as np
import matplotlib.pyplot as plt

from numpy.fft import fft, ifft, fftshift, ifftshift, fftfreq

N = 4096
T = 10
dt = T / N

t = np.linspace(-T/2, T/2, N, endpoint=False)

f = fftshift(fftfreq(N, dt))

def rect():
    x = t
    x = (abs(x) <= 0.5).astype(float)

    return x

def barlett():
    x = t
    x = (1 - 2 * abs(x)) * (abs(x) <= 0.5)

    return x

def hann():
    x = t
    x = (0.5 + 0.5 * np.cos(2 * np.pi * x)) * (abs(x) <= 0.5)

    return x

def hamming():
    x = t
    x = (0.54 + 0.46 * np.cos(2 * np.pi * x)) * (abs(x) <= 0.5)

    return x
def fourier(function):
    return dt * np.real(fftshift(fft(ifftshift(function))))

def plot(window):
    plt.plot(t, window)
    plt.xlim(-0.6, 0.6)
    plt.show()

    plt.plot(f, fourier(window))
    plt.xlim(-2*T, 2*T)
    plt.show()

    plt.plot(f, fourier(window))
    plt.xlim(0, 3*T)
    plt.yscale('log')
    plt.show()

    plt.plot(f, fourier(window))
    plt.xlim(0.1, 100)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

plot(hann())