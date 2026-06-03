import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 4, 5])
r = np.array([1, 1, 1])

nx = np.arange(0, len(x))
nr = np.arange(-1, len(r) - 1)

z = np.convolve(x, r)

nz_start = nx[0] + nr[0]
nz = np.arange(nz_start, nz_start + len(z))

fig, axs = plt.subplots(3, 1, figsize=(8, 10), sharex=True)

axs[0].stem(nx, x, linefmt='b-', markerfmt='bo', basefmt='k-')
axs[0].set_title('Signal x[n]')
axs[0].set_ylabel('Amplitude')
axs[0].grid(True, alpha=0.3)

axs[1].stem(nr, r, linefmt='g-', markerfmt='go', basefmt='k-')
axs[1].set_title('Rectangle Signal r[n]')
axs[1].set_ylabel('Amplitude')
axs[1].grid(True, alpha=0.3)

axs[2].stem(nz, z, linefmt='r-', markerfmt='ro', basefmt='k-')
axs[2].set_title('Convolution z[n] = (x * r)[n]')
axs[2].set_xlabel('Time index (n)')
axs[2].set_ylabel('Amplitude')
axs[2].grid(True, alpha=0.3)

for ax in axs:
    ax.axvline(x=0, color='k', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()