import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

num = [1, 1]
denom = [1, 3, 2]

sys = signal.TransferFunction(num, denom)

w, mag, phase = signal.bode(sys)

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

ax1.semilogx(w, mag)
ax2.semilogx(w, phase)

ax1.set_ylabel("Magnitude")
ax2.set_ylabel("Phase")
ax1.set_xlabel("Frequency")
ax2.set_xlabel("Frequency")
ax1.grid()
ax2.grid()

plt.show()
