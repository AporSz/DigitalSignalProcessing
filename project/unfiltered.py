import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

from project.utils.utils import load

matplotlib.use('TkAgg')

def plot_filtered(time, values):
    smoothed = savgol_filter(values, 51, 3)
    plt.plot(time, smoothed)

def plot_sensor(sensor, filtered = True):
    if np.array(data[sensor]).shape.__len__() == 1:
        if filtered:
            plot_filtered(data["time"], data[sensor])
        else:
            plt.plot(data["time"], data[sensor])
        return

    for i in range(len(data[sensor])):
        if filtered:
            plot_filtered(data["time"], data[sensor][i])
        else:
            plt.plot(data["time"], data[sensor][i])

data = load('data/1_CO2_raw_data/new_device_column1.txt', limit=1000000)

plot_sensor("pressure_top", True)

plt.show()