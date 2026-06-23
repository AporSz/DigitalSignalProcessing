import numpy as np
import matplotlib.pyplot as plt

num = [1, 0.5, 1]
denom = [1, -1.5, 0.7]

zeros = np.roots(num)
poles = np.roots(denom)

theta = np.linspace(0, 2 * np.pi, 100)

fig, ax = plt.subplots(figsize=(6,6))

ax.plot(np.cos(theta), np.sin(theta), 'k--')
ax.scatter(np.real(zeros), np.imag(zeros), marker='o')
ax.scatter(np.real(poles), np.imag(poles), marker='x')

ax.set_aspect('equal')

plt.show()

stable = True

for i in poles:
    if np.abs(i) > 1:
        stable = False

if stable:
    print("System stable")
else:
    print("System unstable")
