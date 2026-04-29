import numpy as np
import matplotlib.pyplot as plt

# 1. Define frequencies to match the visual phase relationship
f_true = 4     # The actual high-frequency continuous signal
f_samp = 5     # The sampling rate

f_alias = abs((f_true + f_samp/2) % f_samp - f_samp/2) # The apparent lower-frequency aliased signal

t_continuous = np.arange(0, 1.5, 0.005)
t_samp = np.arange(0, 1.5, 1/f_samp)

x_true = np.cos(2 * np.pi * f_true * t_continuous)
x_alias = np.cos(2 * np.pi * f_alias * t_continuous)

x_samp = np.cos(2 * np.pi * f_alias * t_samp)

plt.plot(t_continuous, x_true, color='red')
plt.plot(t_continuous, x_alias, color='black')
plt.plot(t_samp, x_samp, 'o', color="black")

plt.show()