import matplotlib
import matplotlib.pyplot as plt

from project.utils.plot_utils import plot_sensor
from project.utils.data_utils import load, get_data_by_minute

matplotlib.use('TkAgg')

N = 100000

# sensor_values = load('data/1_CO2_raw_data/new_device_column1.txt', limit = N)
sensor_values = get_data_by_minute('data/1_CO2_raw_data/data.csv')

time = sensor_values["Timestamp"]

plot_sensor(sensor_values, time, "CO2_main", filtered = False, mark_period = "Month")

plt.show()
from project.utils.plot_utils import plot_sensor, plot_correlation, correlation_matrix
from project.utils.data_utils import load, get_data_by_minute, load_csv

# matplotlib.use('TkAgg')

N = 1000000

# sensor_values = load('data/1_CO2_raw_data/new_device_column1.txt', limit = N)
# sensor_values = get_data_by_minute('data/1_CO2_raw_data/data.csv')
sensor_values = load_csv('data/1_CO2_raw_data/data.csv', N)

time = sensor_values["Timestamp"]

# plot_sensor(sensor_values, time, "CO2_main", filtered = False, mark_period = "Month")

plot_correlation(sensor_values, "Temperature_main", "Temperature_side")
correlation_matrix(sensor_values, ["Temperature_main", "Temperature_side"])
