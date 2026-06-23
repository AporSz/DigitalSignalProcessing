import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-2, 2, 400)
y = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

X_z = np.zeros_like(Z, dtype=complex)
nr_of_terms = 100

for i in range(nr_of_terms):
    z = np.where(Z == 0, 1e-10, Z)
    X_z += (0.5 ** i) * (z ** (-i))

mag = np.abs(X_z)
mag_capped = np.clip(mag, 0, 10)

fig, ax = plt.subplots()

heatmap = ax.pcolormesh(X, Y, mag_capped, cmap='magma', shading='auto')
cbar = plt.colorbar(heatmap)

theta = np.linspace(0, 2 * np.pi, 400)
plt.plot(np.cos(theta) * 0.5, np.sin(theta) * 0.5, 'w--')

plt.show()
