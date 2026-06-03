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

def plot_sensor(data, time, sensor, filtered = False, mark_period = None, color = "blue", index = -1):
    if mark_period is not None:
        add_vertical_line(data, time, sensor, mark_period)

    d = np.array(data[sensor])
    if index >= 0:
        if np.array(data[sensor]).shape.__len__() != 1:
            d = np.array(data[sensor][index])

    if d.shape.__len__() == 1:
        if filtered:
            plot_filtered(time, d, color = color)
        else:
            plt.plot(time, d, color = color)

    else:
        cmap = plt.get_cmap('plasma')
        colors = cmap(np.linspace(1, 0, len(data[sensor])))

        for i in range(len(data[sensor])):
            if filtered:
                plot_filtered(time, data[sensor][i], color=colors[i])
            else:
                plt.plot(time, data[sensor][i], color=colors[i])

    plt.show()

def plot_correlation(data, sensor1, sensor2, index1= -1, index2= -1):
    # Safely extract x data
    d1 = np.array(data[sensor1])
    if d1.ndim == 2:
        x = d1[index1]
        if index1 != -1:
            label1 = f"{sensor1}_{index1}"
        else:
            label1 = sensor1
    else:
        x = d1
        label1 = sensor1

    # Safely extract y data
    d2 = np.array(data[sensor2])
    if d2.ndim == 2:
        y = d2[index2]
        if index2 != -1:
            label2 = f"{sensor2}_{index2}"
        else:
            label2 = sensor2
    else:
        y = d2
        label2 = sensor2

    r_value = np.corrcoef(x, y)[0, 1]

    # plt.figure(figsize=(7, 5))
    
    # 1. Create the hexbin map (better for lots of data points)
    plt.hexbin(x, y, gridsize=50, cmap='Blues', mincnt=1)
    cb = plt.colorbar()
    cb.set_label('Number of Data Points')

    # 2. Add the trendline on top
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m * x + b, color='red', linestyle='--', label=f'Trendline (r={r_value:.3f})')

    # 3. Format the plot
    plt.title(f'Correlation: {label1} vs {label2}')
    plt.xlabel(label1)
    plt.ylabel(label2)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.5)

    plt.show()

def correlation_matrix(data, sensors):
    arrays = []
    labels = []

    for sensor in sensors:
        sensor_data = np.array(data[sensor])
        
        # If it's a 1D array (like Pressure_Top)
        if sensor_data.ndim == 1:
            arrays.append(sensor_data)
            labels.append(sensor)
        
        # If it's a 2D array (like CO2_main with 20 sensors)
        elif sensor_data.ndim == 2:
            for i in range(sensor_data.shape[0]):
                arrays.append(sensor_data[i])
                labels.append(f"{sensor}_{i+1}")

    # Stack all arrays into a single 2D matrix
    matrix = np.vstack(arrays)

    # Compute correlation coefficient matrix
    cm = np.corrcoef(matrix)

    plt.figure(figsize=(10, 8)) # Make the plot a bit larger for many sensors
    plt.imshow(cm, cmap='coolwarm', vmin=-1, vmax=1)
    
    # Add a colorbar so we know what the colors mean (-1 to 1)
    plt.colorbar(label='Correlation Coefficient (r)')
    
    # Add labels to the ticks so we know which sensor is which
    plt.xticks(ticks=np.arange(len(labels)), labels=labels, rotation=90) # Rotate for readability
    plt.yticks(ticks=np.arange(len(labels)), labels=labels)
    plt.title("Sensor Correlation Matrix")
    plt.tight_layout() # Ensure labels aren't cut off
    plt.show()