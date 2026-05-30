import csv

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

#CSV header: Timestamp,Pressure_Top,Humidity_Top,Temperature_Top,Pressure_Bottom,Humidity_Bottom,Temperature_Bottom,CO2_main1,Temperature_main1,CO2_main2,Temperature_main2,CO2_main3,Temperature_main3,CO2_main4,Temperature_main4,CO2_main5,Temperature_main5,CO2_main6,Temperature_main6,CO2_main7,Temperature_main7,CO2_main8,Temperature_main8,CO2_main9,Temperature_main9,CO2_main10,Temperature_main10,CO2_main11,Temperature_main11,CO2_main12,Temperature_main12,CO2_main13,Temperature_main13,CO2_main14,Temperature_main14,CO2_main15,Temperature_main15,CO2_main16,Temperature_main16,CO2_main17,Temperature_main17,CO2_main18,Temperature_main18,CO2_main19,Temperature_main19,CO2_main20,Temperature_main20,CO2_side1,Temperature_side1,CO2_side2,Temperature_side2,CO2_side3,Temperature_side3,CO2_side4,Temperature_side4
def convert_txt_to_csv(path_txt, path_csv):
    with open(path_txt) as f:
        index = 0
        invalid = 0
        line = None
        while not f.closed:
            if index % 1000000 == 0:
                print("1 million processed")

            try:
                line = f.readline()

                if line == "":
                    raise EOFError("Finished reading the file")

                l = line.strip().split()
                t = float(l[0])

                line = f.readline()
                l = line.strip()[2:].split()
                if len(l) <= 2:
                    raise ValueError("Invalid data entry")

                pressure_top, humidity_top, temperature_top = float(l[0]), float(l[1]), float(l[2])

                pressure_bottom, humidity_bottom, temperature_bottom = float(l[3]), float(l[4]), float(l[5])

                co2_main, co2_side, temperature_main, temperature_side = [], [], [], []

                for i in range(3, 3 + 20):
                    co2 = float(l[2 * i])
                    temperature = float(l[2 * i + 1])
                    co2_main.append(co2)
                    temperature_main.append(temperature)

                for i in range(3 + 20, 3 + 20 + 4):
                    c02 = float(l[2 * i])
                    temperature = float(l[2 * i + 1])
                    co2_side.append(c02)
                    temperature_side.append(temperature)

                sensors_main, sensors_side = [], []

                for i in range(20):
                    sensors_main.append(co2_main[i])
                    sensors_main.append(temperature_main[i])

                for i in range(4):
                    sensors_side.append(co2_side[i])
                    sensors_side.append(temperature_side[i])

                with open(path_csv, "a") as csvfile:
                    writer = csv.writer(csvfile)

                    writer.writerow([t, pressure_top, humidity_top, temperature_top, pressure_bottom, humidity_bottom, temperature_bottom] + sensors_main + sensors_side)

            except IndexError as e:
                print(e)
                invalid += 1

            except ValueError as e:
                # print(e)
                invalid += 1
                # print(line)

            except EOFError as e:
                f.close()

            except Exception as e:
                print(e.__class__)

            index += 1

        print("DONE")
        print(f"Number of invalid entries: {invalid} out of {index}")

def convert_csv_to_bin(path_csv, path_bin):
    with open(path_csv) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')

        index = 0

        for row in reader:
            if index % 1000000 == 0:
                print("1 million processed")

            time = float(row["Timestamp"])
            pressure_top = float(row["Pressure_Top"])
            humidity_top = float(row["Humidity_Top"])
            temperature_top = float(row["Temperature_Top"])
            pressure_bottom = float(row["Pressure_Bottom"])
            humidity_bottom = float(row["Humidity_Bottom"])
            temperature_bottom = float(row["Temperature_Bottom"])
            co2_main = []
            temperature_main = []
            for i in range(1, 21):
                co2_main.append(float(row["CO2_main" + str(i)]))
                temperature_main.append(float(row["Temperature_main" + str(i)]))

            co2_side = []
            temperature_side = []
            for i in range(1, 5):
                co2_side.append(float(row["CO2_side" + str(i)]))
                temperature_side.append(float(row["Temperature_side" + str(i)]))

            with open(path_bin, "ab") as binary_file:
                arr = [time, pressure_top, humidity_top, temperature_top, pressure_bottom, humidity_bottom, temperature_bottom]
                arr += co2_main
                arr += temperature_main
                arr += co2_side
                arr += temperature_side

                byte_array = np.array(arr).tobytes()
                binary_file.write(byte_array)

            index += 1

        print("DONE")

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

            except IndexError as e:
                print(e)

            except ValueError as e:
                # print(e)
                pass

            except EOFError as e:
                f.close()

            except Exception as e:
                print(e.__class__)

        return data

# data = load('data/1_CO2_raw_data/new_device_column1.txt')
#
# for i in range(0, 20):
#     plt.plot(data["time"], data["co2_main"][i], label="co2")
#
# plt.show()
#
# for i in range(0, 4):
#     plt.plot(data["time"], data["co2_side"][i], label="co2")
#
# plt.show()
#
# for i in range(0, 20):
#     plt.plot(data["time"], data["temperature_main"][i], label="co2")
#
# plt.show()
#
# for i in range(0, 4):
#     plt.plot(data["time"], data["temperature_side"][i], label="co2")
#
# plt.show()

# convert_txt_to_csv('data/1_CO2_raw_data/new_device_column1.txt', 'data/1_CO2_raw_data/data.csv')
# convert_txt_to_csv('data/1_CO2_raw_data/chunk_00.txt', 'data/1_CO2_raw_data/data.csv')

convert_csv_to_bin('data/1_CO2_raw_data/data.csv', 'data/1_CO2_raw_data/data.bin')