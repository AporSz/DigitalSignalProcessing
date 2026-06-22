import csv
import os
import numpy as np

CSV_FIELDNAMES = (
    ["Timestamp", "Pressure_Top", "Humidity_Top", "Temperature_Top", "Pressure_Bottom", "Humidity_Bottom", "Temperature_Bottom"]
    + [name for i in range(1, 21) for name in (f"CO2_main{i}", f"Temperature_main{i}")]
    + [name for i in range(1, 5) for name in (f"CO2_side{i}", f"Temperature_side{i}")]
)

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

                write_header = not os.path.exists(path_csv) or os.path.getsize(path_csv) == 0
                with open(path_csv, "a", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    if write_header:
                        writer.writerow(CSV_FIELDNAMES)
                with open(path_csv, "a", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([t, pressure_top, humidity_top, temperature_top, pressure_bottom, humidity_bottom, temperature_bottom] + sensors_main + sensors_side)

            except IndexError as e:
                invalid += 1
            except ValueError as e:
                invalid += 1
            except EOFError as e:
                f.close()
            except Exception as e:
                print(e.__class__)

            index += 1

        print("DONE")
        print(f"Number of invalid entries: {invalid} out of {index}")

def convert_csv_to_bin(path_csv, path_bin):
    with open(path_csv, 'r') as csvfile:
        with open(path_bin, "wb") as binary_file:
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

                sensor_array = [pressure_top, humidity_top, temperature_top, pressure_bottom, humidity_bottom, temperature_bottom]
                sensor_array += co2_main
                sensor_array += temperature_main
                sensor_array += co2_side
                sensor_array += temperature_side

                time_array = np.array([time], dtype=np.float64).tobytes()
                byte_array = time_array + np.array(sensor_array, dtype=np.float32).tobytes()
                binary_file.write(byte_array)
                index += 1

    print("DONE")
