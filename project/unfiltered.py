import numpy as np

def load(path):
    data = {
        "time": [],
        "pressure_top" : [],
        "humidity_top" : [],
        "temperature_top" : [],
        "pressure_bottom" : [],
        "humidity_bottom" : [],
        "temperature_bottom" : [],
        "co2_main" : [],
        "co2_side" : [],
    }
    with open(path) as f:
        while not f.closed:
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

                for i in range(6, 6 + 40):
                    co2 = float(l[i])
                    data["co2_main"].append(co2)

                for i in range(6 + 40, 6 + 40 + 8):
                    c02 = float(l[i])
                    data["co2_side"].append(c02)
            except Exception as e:
                # print(e)
                continue

        return data

data = load('data/1_CO2_raw_data/new_device_column1.txt')
print(data)