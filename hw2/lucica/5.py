import numpy as np

x = np.array([1, 2, 3, 2, 1])
y = np.array([-1, 2, 1])

N = len(x)
M = len(y)
z_len = N + M - 1

z_a = np.zeros(z_len)
for n in range(z_len):
    s = 0
    for k in range(max(n - M + 1, 0), min(n + 1, N)):
        s += x[k] * y[n - k]
    z_a[n] = s

print("Result (a) Explicit Loops:       ", z_a)

z_b = np.zeros(z_len)
for n in range(z_len):
    k = np.arange(max(n - M + 1, 0), min(n + 1, N))
    z_b[n] = (x[k] * y[n - k]).sum()

print("Result (b) Mixed Vectorization:  ", z_b)

i, j = np.arange(z_len), np.arange(N)
I, J = np.meshgrid(j, i)
tmp = J - I

tmp[tmp >= M] = -1
ind = np.where(tmp >= 0)

H = np.zeros([z_len, N], dtype=int)
H[ind] = y[tmp[ind]]

z_c = np.array(np.mat(H) * np.mat(x).T).flatten()

print("Result (c) Fully Vectorized:     ", z_c)

z_ref = np.convolve(x, y)
print("numpy.convolve output:           ", z_ref)

all_match = np.allclose(z_a, z_ref) and np.allclose(z_b, z_ref) and np.allclose(z_c, z_ref)
print(f"\nDo all implementations match numpy? {all_match}")