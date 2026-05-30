import matplotlib
import matplotlib.pyplot as plt

from project.utils.plot_utils import plot_sensor
from project.utils.data_utils import load

matplotlib.use('TkAgg')

N = 100000

sensor_values = load('data/1_CO2_raw_data/new_device_column1.txt', limit = N)

plot_sensor(sensor_values,"CO2_main", filtered = False, mark_days = True)

plt.show()