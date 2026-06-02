import numpy as np
from scipy.signal import savgol_filter

def filter_data(data):
    for sensor,values in data.items():
        if sensor != "Timestamp":
            data[sensor] = savgol_filter(values, 51, 3)

def filter_values(values):
    return savgol_filter(values, 51, 3)