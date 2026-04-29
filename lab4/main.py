import numpy as np
import matplotlib.pyplot as plt

# T = 0.15
# we need 0.13 because need an od number of ones in the rectangle
# (odd number of ones after: print(abs(t) < 0.5) )
T = 0.13

t = np.arange(-10, 10, T)
rect = np.zeros(len(t))

rect[abs(t) < 0.5] = 1

# print(abs(t) < 0.5)
#
# print((abs(t) < 0.5).astype(int))

rect1 = (abs(t) < 0.5).astype(int)

# print((rect == rect1).sum())

# plt.plot(t,rect, '.-')
Frect = T * np.fft.fft(rect)

f = np.fft.fftfreq(len(rect), T)

# plt.plot(np.fft.fftshift(f), np.fft.fftshift(np.real(Frect)), '.-')

tri = np.zeros(len(t))
tri[abs(t) <= 0.5] = (1 - abs(t)/0.5)[abs(t) <= 0.5]

plt.plot(t, tri, '.-')

Ftri = T * np.fft.fft(tri)
plt.plot(np.fft.fftshift(f), np.fft.fftshift(abs(Ftri)), '.-')

plt.show()