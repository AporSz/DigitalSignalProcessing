import numpy as np

# 5. Write a script for calculating the convolution of the two sequences
# (a) only explicit loops (no vector operations)
# (b) external explicit loop, internal loop using vector operation
# (c) using only vector operations
# Compare it to the numpy.convolve output.

X = np.array([1, 2, -1, 3, 1, 0, 2])
Y = np.array([1, 2, -1])

def convolve_a(x, h):
    length = (len(x) + len(h) - 1)

    y = []
    for i in range(length):
        y.append(0)

    for n in range(length):
        for k in range(len(x)):
            if 0 <= n - k < len(h):
                y[n] += x[k] * h[n - k]

    return y

def convolve_b(x, h):
    y = np.zeros(len(x) + len(h) - 1)
    for n in range(len(y)):
        k = np.arange(max(n - len(h) + 1, 0), min(n + 1, len(x)))
        y[n] = (x[k] * h[n - k]).sum()
    return y

def convolve_c(x, h):
    n = len(x)
    m = len(h)
    i = np.arange(n+m-1)
    j = np.arange(n)

    I, J = np.meshgrid(j, i)

    aux = J - I
    aux[ aux >= m] = -1

    ind = np.where(aux >= 0)

    H = np.zeros([n + m -1, n], dtype=int)
    H[ind] = h[aux[ind]]

    return (np.mat(H) * np.mat(x).T).flatten()

print(convolve_a(X, Y))
print(convolve_b(X, Y))
print(convolve_c(X, Y))
print(np.convolve(X, Y))

# 6. Write a script that displays the stemplots of the signal x[n] = {1, 2, 3, 4, 5}, and the rectangle signal r[n] =
# {1, 1, 1} along with that of their convolution. Time-origin (n = 0) indices are in bold. The plots should be on
# the same figure, properly positioned with respect to the time-origin.

