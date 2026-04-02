from pylab import *

import matplotlib.pyplot as plt

# def ditfft2(x):
#     N = len(x)
#     if N == 1:
#         return x
#     even = ditfft2(x[::2])
#     odd = exp(-2*pi*1j/N) * arange(N/2) * ditfft2(x[1::2])
#     return hstack([even + odd, even - odd])
#
# x = arange(16)
# print(ditfft2(x))

N = 512 #128
tmax = 2
tm = 1.0
T = 2 * tmax/N
t = arange(-tmax, tmax, T)
x = zeros(N)
x[abs(t) <= tm] = (1 - abs(t)/tm)[abs(t) <= tm]
plot(t, x, '.-')
show()

x = fftshift(x)
X = T * fft(x, N)
f = fftfreq(N, T)

plot(fftshift(f), fftshift(real(X)), '.-')
## xlim([-16,16])
show()

N = 128
x = zeros(N)
# x[abs(t) <= tm] = (1 - abs(t)/tm)[abs(t) <= tm]

Npad = 512

xp = pad(x, ((Npad - N)//2, (Npad - N)//2))

tpmax = tmax * Npad // N
tp = arange(-tpmax, tpmax, T)
plot(t, x, '.-')
show()