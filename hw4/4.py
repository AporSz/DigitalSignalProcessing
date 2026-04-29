import numpy as np
import matplotlib.pyplot as plt

from numpy.fft import fft, ifft, fftshift, ifftshift, fftfreq

N = 1024
T = 20
dt = T / N

t = np.linspace(-T/2, T/2, N, endpoint=False)

f = fftshift(fftfreq(N, dt))

def timeA():
    x = np.exp(- t ** 2)

    return x

def freqA():
    x = np.sqrt(np.pi ) * np.exp(- np.pi ** 2 * f ** 2)

    return x

def timeB():
    x = t
    x = (abs(x) <= 0.5).astype(float)

    return x

def freqB():
    x = np.sinc(f)

    return x

# the anomaly occurs because we cut the sinc function. we only take a window of it, not the full function
# since we can't take infinite values
def timeC():
    x = np.sinc(t)

    return x

def freqC():
    x = f
    x = (abs(x) <= 0.5).astype(float)

    return x

# This is an extreme case of time-domain truncation (spectral leakage), caused by the slow decay of your time-domain
# signal.The Slow Decay: In part (a), your function was $e^{-t^2}$, which drops to near-zero instantly. But in part (d),
# your function is $\frac{1}{1+t^2}$. This decays very slowly. At the very edge of your time window ($t = 10$ and $t = -10$),
# the value is still $1 / (1 + 100) \approx 0.01$.The Sharp Cutoff: Because your array just stops at $t=10$, you are
# effectively chopping off the tails of the function. It instantly drops from $0.01$ to $0$.The Frequency Consequence:
# The FFT assumes your signal is periodic. A sudden jump at the boundaries acts like a sharp, rectangular edge. As we
# learned in part (c), sharp edges in the time domain create high-frequency ripples (sinc waves) in the frequency domain.
def timeD():
    x = 1 / (1 + t ** 2)

    return x

def freqD():
    x = np.pi * np.exp(-2 * np.pi * abs(f))

    return x

# The anomaly in part (e) is a very low-level noise floor at high frequencies caused by time-domain truncation. Because
# the function $e^{-|t|}$ decays exponentially fast, its value at the boundaries of the finite time window is practically
# zero. Consequently, chopping off the infinite tails of the function creates only a microscopic discontinuity, resulting
# in extremely minimal spectral leakage.
def timeE():
    x = np.exp(- abs(t))

    return x

def freqE():
    x = 2 / (1 + 4 * (np.pi ** 2) * (f **2))

    return x

def draw(time, freq):
    plt.plot(f, np.real(dt * fftshift(fft(ifftshift(time())))), '.')
    plt.xscale('log')
    plt.yscale('log')
    plt.plot(f, freq())
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

    plt.plot(t, time())
    plt.plot(t, 1 / dt * np.real(fftshift(ifft(ifftshift(freq())))), '.')
    plt.show()

draw(timeE, freqE)