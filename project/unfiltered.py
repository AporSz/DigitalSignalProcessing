import csv

import numpy as np
import matplotlib.pyplot as plt

def convert_to_csv(path_txt, path_csv):
    with open(path_txt) as f:
        while not f.closed:
            try:
                line = f.readline()
                l = line.strip().split()
                t = float(l[0])

                line = f.readline()
                l = line.strip()[2:].split()
                if len(l) <= 2:
                    raise ValueError("Invalid data entry")

                pressure_top, humidity_top, temperature_top = float(l[0]), float(l[1]), float(l[2])

                pressure_bottom, humidity_bottom, temperature_bottom = float(l[3]), float(l[4]), float(l[5])

                co2_main, co2_side = [], []

                for i in range(6, 6 + 40):
                    co2_main.append(float(l[i]))

                for i in range(6 + 40, 6 + 40 + 8):
                    co2_side.append(float(l[i]))

                with open(path_csv, "a") as csvfile:
                    writer = csv.writer(csvfile)

                    writer.writerow([t, pressure_top, humidity_top, temperature_top, pressure_bottom, humidity_bottom, temperature_bottom] + co2_main + co2_side)

            except Exception as e:
                # print(e)
                continue

def load(path, limit = 100000):
    data = {
        "time": [],
        "pressure_top" : [],
        "humidity_top" : [],
        "temperature_top" : [],
        "pressure_bottom" : [],
        "humidity_bottom" : [],
        "temperature_bottom" : [],
        "co2_main" : [],
        "temperature_main" : [],
        "co2_side" : [],
        "temperature_side" : [],
    }

    for i in range(3, 3 + 20):
        data["co2_main"].append([])
        data["temperature_main"].append([])

    for i in range(3 + 20, 3 + 20 + 4):
        data["co2_side"].append([])
        data["temperature_side"].append([])

    index = 0
    with open(path) as f:
        while not f.closed and index < limit:
            try:
                line = f.readline()
                l = line.strip().split()
                t = float(l[0])

                line = f.readline()
                l = line.strip()[2:].split()
                if len(l) <= 2:
                    raise ValueError("Line not containing enough data")

                data["time"].append(t)

                pressure, humidity, temperature = float(l[0]), float(l[1]), float(l[2])
                data["pressure_top"].append(pressure)
                data["humidity_top"].append(humidity)
                data["temperature_top"].append(temperature)

                pressure, humidity, temperature = float(l[3]), float(l[4]), float(l[5])
                data["pressure_bottom"].append(pressure)
                data["humidity_bottom"].append(humidity)
                data["temperature_bottom"].append(temperature)

                for i in range(3, 3 + 20):
                    co2 = float(l[2 * i])
                    temperature = float(l[2 * i + 1])
                    data["co2_main"][i - 3].append(co2)
                    data["temperature_main"][i - 3].append(temperature)

                for i in range(3 + 20, 3 + 20 + 4):
                    c02 = float(l[2 * i])
                    temperature = float(l[2 * i + 1])
                    data["co2_side"][i - 20 - 3].append(c02)
                    data["temperature_side"][i - 20 - 3].append(temperature)

                index += 1
            except Exception as e:
                # print(e)
                continue

        return data

data = load('data/1_CO2_raw_data/new_device_column1.txt')

for i in range(0, 20):
    plt.plot(data["time"], data["co2_main"][i], label="co2")

plt.show()

for i in range(0, 4):
    plt.plot(data["time"], data["co2_side"][i], label="co2")

plt.show()