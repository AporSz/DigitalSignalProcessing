import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

from project.utils.data_utils import load

def plot_filtered(time, values, color):
    smoothed = savgol_filter(values, 51, 3)
    plt.plot(time, smoothed, color = color)

def add_vertical_line(data, sensor):
    ymin = np.array(data[sensor]).flatten().min()
    ymax = np.array(data[sensor]).flatten().max()
    xmin = np.array(data["Timestamp"]).flatten().min()
    xmax = np.array(data["Timestamp"]).flatten().max()
    vertical_lines = np.arange(xmin, xmax)[::86400]
    plt.vlines(vertical_lines, ymin=ymin, ymax=ymax, colors='grey')

def plot_sensor(data, sensor, filtered = False, mark_days = False, color = "blue"):
    if mark_days:
        add_vertical_line(data, sensor)

    if np.array(data[sensor]).shape.__len__() == 1:
        if filtered:
            plot_filtered(data["Timestamp"], data[sensor], color = color)
        else:
            plt.plot(data["Timestamp"], data[sensor], color = color)

        return

    cmap = plt.get_cmap('plasma')
    colors = cmap(np.linspace(1, 0, len(data[sensor])))

    for i in range(len(data[sensor])):
        if filtered:
            plot_filtered(data["Timestamp"], data[sensor][i], color = colors[i])
        else:
            plt.plot(data["Timestamp"], data[sensor][i], color = colors[i])