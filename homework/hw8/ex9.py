import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

num = [1, 1]
denom = [1, 3, 2]

w_start = -2
w_stop = 2

w = np.logspace(w_start, w_stop, 1000)
s = 1j * w

num_eval = np.polyval(num, s)
denom_eval = np.polyval(denom, s)

H = num_eval / denom_eval

mag_manual = 20 * np.log10(np.abs(H))
phase_manual = np.angle(H, deg=True)

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

ax1.semilogx(w, mag_manual, label = "Manual")
ax2.semilogx(w, phase_manual, label = "Manual")

sys = signal.TransferFunction(num, denom)

w_bode, mag_bode, phase_bode = signal.bode(sys, w)

ax1.semilogx(w_bode, mag_bode, 'k--', label = "Scipy bode")
ax2.semilogx(w_bode, phase_bode, 'k--', label = "Scipy bode")

# add labels with ax1.set_xlabel("Something") ax1.set_ylabel("Something else")

ax1.grid()
ax2.grid()
ax1.legend()
ax2.legend()

plt.show()
