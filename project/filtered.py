import numpy as np

filtered_data = np.load('data/2_CO2_cleand_data/new_device_all_data_filterd.npy')

print(len(filtered_data))

for i in range(len(filtered_data)):
    print(len(filtered_data[i]))