import numpy as np
import matplotlib.pyplot as plt

t = np.arange(-10, 10, 0.1)
rect = np.zeros(len(t))

rect[abs(t) < 0.5] = 1

# print(abs(t) < 0.5)
#
# print((abs(t) < 0.5).astype(int))

rect1 = (abs(t) < 0.5).astype(int)

# print((rect == rect1).sum())

# plt.plot(t,rect, '.-')
Frect = 0.1 * np.fft.fft(rect)

f = np.fft.fftfreq(len(rect), 0.1)

# plt.plot(np.fft.fftshift(f), np.fft.fftshift(abs(Frect)), '.-')

tri = np.zeros(len(t))
tri[abs(t) <= 0.5] = (1 - abs(t)/0.5)[abs(t) <= 0.5]

plt.plot(t, tri, '.-')

Ftri = 0.1 * np.fft.fft(tri)
plt.plot(np.fft.fftshift(f), np.fft.fftshift(abs(Ftri)), '.-')

plt.show()