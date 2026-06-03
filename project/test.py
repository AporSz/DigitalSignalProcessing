import numpy as np
import matplotlib.pyplot as plt

# 1. Define the arrays
x = np.array([1, 3, 6, 7])
y = np.array([2, 4, 5, 8])

# 2. Calculate the correlation coefficient
# np.corrcoef returns a matrix, so we grab the value at [0, 1]
r_value = np.corrcoef(x, y)[0, 1]
print(f"The correlation coefficient (r) is: {r_value}")

# 3. Create the scatter plot
plt.figure(figsize=(6, 4))
plt.scatter(x, y, color='blue', s=100, label='Data Points')

# 4. Add a trendline to visualize the correlation perfectly
m, b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b, color='red', linestyle='--', label=f'Trendline (r={r_value})')

# 5. Format the plot
plt.title('Scatter Plot Showing Perfect Positive Correlation')
plt.xlabel('Array 1 (X)')
plt.ylabel('Array 2 (Y)')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)

# Display the plot
plt.show()