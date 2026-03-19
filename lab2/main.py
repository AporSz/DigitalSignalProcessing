from pylab import *
import numpy as np
import matplotlib.pyplot as plt

X = np.array([1, 2, -1, 3, 1, 0, 2])
H = np.array([1, 2, -1])

def convolve(x, h):
    length = (len(x) + len(h) - 1)

    y = [0] * length

    for n in range(length):
        for k in range(len(x)):
            if 0 <= n - k < len(h):
                y[n] += x[k] * h[n - k]

    return y

N = 10

impulse = [0] * N

# print(convolve(X, H))

# print(roll(impulse,N//2))

# numbers = np.arange(N)

# impulse = zeros(N)
# impulse[0] = 1

# numbers = np.arange(N) - N//2
# print(impulse[numbers]) #prints the numbers from impulse with indeces present in numbers

# unit = zeros(N)
# unit[:N//2] = 1

# print(unit)

def convolve_np(x, y):
    z = np.zeros(len(x) + len(y) - 1)
    for n in range(len(z)):# explicit Python loop
        k = np.arange(max(n - len(y)+1, 0), min(n+1, len(x))) # vectorized op.
        z[n] = (x[k]*y[n-k]).sum() # vectorized op.
    return z

print(convolve_np(X,H))


plt.stem(impulse)
plt.show()