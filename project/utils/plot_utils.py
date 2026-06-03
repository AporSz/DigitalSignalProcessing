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