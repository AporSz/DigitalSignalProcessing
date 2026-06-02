import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

from project.utils.data_utils import load

def plot_filtered(time, values, color):
    smoothed = savgol_filter(values, 51, 3)
    plt.plot(time, smoothed, color = color)

def add_vertical_line(data, time, sensor, period):
    ymin = np.array(data[sensor]).flatten().min()
    ymax = np.array(data[sensor]).flatten().max()
    xmin = np.array(time).flatten().min()
    xmax = np.array(time).flatten().max()
    if period == "Day":
        vertical_lines = np.arange(xmin, xmax)[::86400]
    elif period == "Week":
        vertical_lines = np.arange(xmin, xmax)[::86400 * 7]
    elif period == "Month":
        vertical_lines = np.arange(xmin, xmax)[::86400 * 30]
    else:
        return
    plt.vlines(vertical_lines, ymin=ymin, ymax=ymax, colors='grey')

def plot_sensor(data, time, sensor, filtered = False, mark_period = None, color = "blue"):
    if mark_period is not None:
        add_vertical_line(data, time, sensor, mark_period)

    if np.array(data[sensor]).shape.__len__() == 1:
        if filtered:
            plot_filtered(time, data[sensor], color = color)
        else:
            plt.plot(time, data[sensor], color = color)

        return

    cmap = plt.get_cmap('plasma')
    colors = cmap(np.linspace(1, 0, len(data[sensor])))

    for i in range(len(data[sensor])):
        if filtered:
            plot_filtered(time, data[sensor][i], color = colors[i])
        else:
            plt.plot(time, data[sensor][i], color = colors[i])

def plot_correlation(data, sensor1, sensor2):
    x = data[sensor1]
    y = data[sensor2]

    r_value = np.corrcoef(x, y)[0, 1]
    print(f"The correlation coefficient (r) is: {r_value}")

    # 3. Create the scatter plot
    plt.figure(figsize=(6, 4))
    plt.scatter(x, y, color='blue', s=100, label='Data Points')

    # 4. Add a trendline to visualize the correlation perfectly
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m * x + b, color='red', linestyle='--', label=f'Trendline (r={r_value})')

    # 5. Format the plot
    plt.title('Scatter Plot Showing Perfect Positive Correlation')
    plt.xlabel('Array 1 (X)')
    plt.ylabel('Array 2 (Y)')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)

    # Display the plot
    plt.show()