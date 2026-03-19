import numpy as np
import matplotlib.pyplot as plt

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

# 1. Define the signals and their exact values
# x[n] = {1, 2, 3, 4, 5} with time-origin at value 2
x_values = np.array([1, 2, 3, 4, 5])
n_x = np.array([-1, 0, 1, 2, 3])

# r[n] = {1, 1, 1} with time-origin at the middle 1
r_values = np.array([1, 1, 1])
n_r = np.array([-1, 0, 1])

# 2. Compute the convolution
y_values = np.convolve(x_values, r_values, mode='full')

# 3. Calculate the time indices for the convolved signal y[n]
# The starting index of the convolution is the sum of the starting indices of x and r
start_n = n_x[0] + n_r[0]
end_n = n_x[-1] + n_r[-1]
n_y = np.arange(start_n, end_n + 1)

# 4. Plotting
# We use subplots with sharex=True to perfectly align the time-axis
fig, axs = plt.subplots(3, 1, figsize=(8, 8), sharex=True)

# Plot x[n]
axs[0].stem(n_x, x_values, basefmt="black")
axs[0].set_title("Signal $x[n]$")
axs[0].set_ylabel("Amplitude")
axs[0].grid(True, linestyle='--', alpha=0.6)

# Plot r[n]
axs[1].stem(n_r, r_values, basefmt="black")
axs[1].set_title("Rectangle Signal $r[n]$")
axs[1].set_ylabel("Amplitude")
axs[1].grid(True, linestyle='--', alpha=0.6)

# Plot y[n]
axs[2].stem(n_y, y_values, basefmt="black")
axs[2].set_title("Convolution $y[n] = x[n] * r[n]$")
axs[2].set_xlabel("Time Index (n)")
axs[2].set_ylabel("Amplitude")
axs[2].grid(True, linestyle='--', alpha=0.6)

# Highlight the time-origin (n=0) across all plots with a subtle red vertical line
for ax in axs:
    # 1. Set the exact numeric locations for the ticks
    ticks = np.arange(-3, 6)
    ax.set_xticks(ticks)

    # 2. Apply bold math formatting to EVERY tick
    # The f-string fr'$\mathbf{{{t}}}$' dynamically inserts each number 't' into the bold tags
    tick_labels = [fr'$\mathbf{{{t}}}$' for t in ticks]

    # 3. Apply the custom bold labels to the axis
    ax.set_xticklabels(tick_labels)

    # (Optional) Keep the red vertical line for the origin
    ax.axvline(x=0, color='red', alpha=0.3, linestyle='-', linewidth=2)

plt.tight_layout()
plt.show()