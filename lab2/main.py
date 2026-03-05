from pylab import *
import numpy as np
## import matplotlib.pyplot as plt

X = [1, 2, -1, 3, 1, 0, 2]
H = [1, 2, -1]

def convolve(x, h):
    length = (len(x) + len(h) - 1)

    y = [0] * length

    for n in range(length):
        for k in range(len(x)):
            if n - k >= 0 and n - k < len(h):
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

def convolve_np(x, h):
    nx, nh = len(x), len(h)
    y = zeros(nx + nh - 1)

    for n in arange(nx + nh - 1):
        k = arange(n - nx + 1, n + 1)
        y[n] = (x[k]*h[n-k]).sum()

print(convolve_np(X,H))



plt.stem(impulse)
plt.show()