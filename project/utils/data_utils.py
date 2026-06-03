import csv
import os

import numpy as np

from numpy import dtype


CSV_FIELDNAMES = (
    ["Timestamp", "Pressure_Top", "Humidity_Top", "Temperature_Top", "Pressure_Bottom", "Humidity_Bottom", "Temperature_Bottom"]
    + [name for i in range(1, 21) for name in (f"CO2_main{i}", f"Temperature_main{i}")]
    + [name for i in range(1, 5) for name in (f"CO2_side{i}", f"Temperature_side{i}")]
)


def _csv_dict_reader(csvfile):
    """Read project CSV with or without a header row; skip blank lines."""
    start = csvfile.tell()
    first_line = csvfile.readline()
    csvfile.seek(start)

    if not first_line.strip():
        csvfile.readline()

    first_cell = first_line.split(",")[0].strip()
    if first_cell == "Timestamp":
        reader = csv.DictReader(csvfile, delimiter=",")
    else:
        reader = csv.DictReader(csvfile, fieldnames=CSV_FIELDNAMES, delimiter=",")

    for row in reader:
        timestamp = (row.get("Timestamp") or "").strip()
        if not timestamp or timestamp == "Timestamp":
            continue
        try:
            float(timestamp)
        except ValueError:
            continue
        yield row


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
    with open(path_csv, 'r', newline='') as csvfile:
        with open(path_bin, "wb") as binary_file:
            index = 0

            for row in _csv_dict_reader(csvfile):
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

# Binary layout produced by convert_csv_to_bin (float64 timestamp + 54 float32 sensors)
SENSOR_VALUE_COUNT = 54
RECORD_SIZE_BYTES = 8 + SENSOR_VALUE_COUNT * 4


def load_bin(path, limit=None):
    """Read records written by convert_csv_to_bin."""
    data = {
        "Timestamp": [],
        "Pressure_Top": [],
        "Humidity_Top": [],
        "Temperature_Top": [],
        "Pressure_Bottom": [],
        "Humidity_Bottom": [],
        "Temperature_Bottom": [],
        "CO2_main": [[] for _ in range(20)],
        "Temperature_main": [[] for _ in range(20)],
        "CO2_side": [[] for _ in range(4)],
        "Temperature_side": [[] for _ in range(4)],
    }

    with open(path, "rb") as binary_file:
        index = 0
        while True:
            if limit is not None and index >= limit:
                break

            record = binary_file.read(RECORD_SIZE_BYTES)
            if not record:
                break
            if len(record) != RECORD_SIZE_BYTES:
                raise ValueError(
                    f"Truncated record at index {index}: expected {RECORD_SIZE_BYTES} bytes, got {len(record)}"
                )

            timestamp = np.frombuffer(record[:8], dtype=np.float64)[0]
            sensors = np.frombuffer(record[8:], dtype=np.float32)

            data["Timestamp"].append(float(timestamp))
            data["Pressure_Top"].append(float(sensors[0]))
            data["Humidity_Top"].append(float(sensors[1]))
            data["Temperature_Top"].append(float(sensors[2]))
            data["Pressure_Bottom"].append(float(sensors[3]))
            data["Humidity_Bottom"].append(float(sensors[4]))
            data["Temperature_Bottom"].append(float(sensors[5]))

            for i in range(20):
                data["CO2_main"][i].append(float(sensors[6 + i]))
                data["Temperature_main"][i].append(float(sensors[26 + i]))
            for i in range(4):
                data["CO2_side"][i].append(float(sensors[46 + i]))
                data["Temperature_side"][i].append(float(sensors[50 + i]))

            index += 1

    return data


def verify_bin_file(path_bin, path_csv=None, sample_checks=5, strict_ranges=False):
    """
    Check that a .bin file matches convert_csv_to_bin layout and contains plausible sensor values.
    Optionally compare the first and last records against path_csv.

    Raw sensor bins may include slight negative CO2 readings; these are reported as warnings
    unless strict_ranges=True (expects cleaned data within 0–100 %).
    """
    path_bin = str(path_bin)
    issues = []
    warnings = []
    file_size = os.path.getsize(path_bin)

    if file_size == 0:
        return {"valid": False, "record_count": 0, "issues": ["File is empty"]}

    if file_size % RECORD_SIZE_BYTES != 0:
        remainder = file_size % RECORD_SIZE_BYTES
        issues.append(
            f"File size {file_size} is not a multiple of record size {RECORD_SIZE_BYTES} (remainder {remainder} bytes)"
        )

    record_count = file_size // RECORD_SIZE_BYTES
    data = load_bin(path_bin)

    timestamps = np.array(data["Timestamp"], dtype=np.float64)
    if len(timestamps) != record_count:
        issues.append(f"Parsed {len(timestamps)} records but size implies {record_count}")

    if not np.all(np.isfinite(timestamps)):
        issues.append("Timestamps contain NaN or Inf")

    if len(timestamps) > 1 and not np.all(np.diff(timestamps) > 0):
        non_monotonic = int(np.sum(np.diff(timestamps) <= 0))
        issues.append(f"Timestamps are not strictly increasing ({non_monotonic} non-increasing steps)")

    flat_values = []
    for key in ["Pressure_Top", "Humidity_Top", "Temperature_Top", "Pressure_Bottom", "Humidity_Bottom", "Temperature_Bottom"]:
        flat_values.extend(data[key])
    for series in data["CO2_main"] + data["Temperature_main"] + data["CO2_side"] + data["Temperature_side"]:
        flat_values.extend(series)

    values = np.array(flat_values, dtype=np.float32)
    if not np.all(np.isfinite(values)):
        issues.append("Sensor values contain NaN or Inf")

    humidity_top = np.array(data["Humidity_Top"], dtype=np.float32)
    humidity_bottom = np.array(data["Humidity_Bottom"], dtype=np.float32)
    co2_values = np.concatenate([np.array(s, dtype=np.float32) for s in data["CO2_main"] + data["CO2_side"]])

    def _range_check(values, label, lo, hi):
        below = int(np.sum(values < lo))
        above = int(np.sum(values > hi))
        if below == 0 and above == 0:
            return
        msg = f"{label} outside {lo}–{hi} % ({below} below, {above} above; min={values.min():.3f}, max={values.max():.3f})"
        if strict_ranges:
            issues.append(msg)
        else:
            warnings.append(msg + " — common in raw data")

    _range_check(humidity_top, "Humidity_Top", 0, 100)
    _range_check(humidity_bottom, "Humidity_Bottom", 0, 100)
    _range_check(co2_values, "CO2", 0, 100)

    if path_csv:
        csv_rows = []
        with open(path_csv, "r", newline="") as csvfile:
            for row in _csv_dict_reader(csvfile):
                csv_rows.append(row)

        if len(csv_rows) != record_count:
            issues.append(f"CSV row count {len(csv_rows)} does not match binary record count {record_count}")
        else:
            indices = [0, record_count - 1]
            if record_count > 2:
                step = max(1, (record_count - 1) // max(1, sample_checks - 1))
                indices.extend(range(step, record_count - 1, step))
            indices = sorted(set(indices))

            for idx in indices:
                row = csv_rows[idx]
                if abs(float(row["Timestamp"]) - data["Timestamp"][idx]) > 1e-3:
                    issues.append(f"Timestamp mismatch at record {idx}")
                if abs(float(row["Pressure_Top"]) - data["Pressure_Top"][idx]) > 1e-2:
                    issues.append(f"Pressure_Top mismatch at record {idx}")

    return {
        "valid": len(issues) == 0,
        "record_count": record_count,
        "first_timestamp": float(timestamps[0]) if len(timestamps) else None,
        "last_timestamp": float(timestamps[-1]) if len(timestamps) else None,
        "issues": issues,
        "warnings": warnings,
    }


def verify_npy_file(path_npy):
    """Check that a cleaned .npy dataset loads and contains finite numeric arrays."""
    issues = []
    try:
        data = np.load(path_npy, allow_pickle=True)
    except Exception as exc:
        return {"valid": False, "issues": [f"np.load failed: {exc}"]}

    series_count = 0
    lengths = []

    if isinstance(data, np.ndarray) and data.dtype == object:
        series_count = len(data)
        for i, series in enumerate(data):
            arr = np.asarray(series)
            if arr.size == 0:
                issues.append(f"Series {i} is empty")
                continue
            if not np.all(np.isfinite(arr)):
                issues.append(f"Series {i} contains NaN or Inf")
            lengths.append(len(arr))

        if lengths and len(set(lengths)) > 1:
            issues.append(f"Inconsistent series lengths: min={min(lengths)}, max={max(lengths)}")
    elif isinstance(data, np.ndarray):
        series_count = 1
        lengths = [data.size]
        if data.size == 0:
            issues.append("Array is empty")
        if not np.all(np.isfinite(data)):
            issues.append("Array contains NaN or Inf")
    else:
        issues.append(f"Unexpected loaded type: {type(data)}")

    return {
        "valid": len(issues) == 0,
        "series_count": series_count,
        "lengths": lengths,
        "issues": issues,
    }


#data from csv file
def get_data_by_minute(path):
    data = {
        "Timestamp": [],
        "Pressure_Top": [],
        "Humidity_Top": [],
        "Temperature_Top": [],
        "Pressure_Bottom": [],
        "Humidity_Bottom": [],
        "Temperature_Bottom": [],
        "CO2_main": [],
        "Temperature_main": [],
        "CO2_side": [],
        "Temperature_side": [],
    }

    for i in range(3, 3 + 20):
        data["CO2_main"].append([])
        data["Temperature_main"].append([])

    for i in range(3 + 20, 3 + 20 + 4):
        data["CO2_side"].append([])
        data["Temperature_side"].append([])

    with open(path, 'r', newline='') as csvfile:
        for index, row in enumerate(_csv_dict_reader(csvfile)):
            if index % 60 == 0:
                data["Timestamp"].append(float(row["Timestamp"]))
                data["Pressure_Top"].append(float(row["Pressure_Top"]))
                data["Humidity_Top"].append(float(row["Humidity_Top"]))
                data["Temperature_Top"].append(float(row["Temperature_Top"]))
                data["Pressure_Bottom"].append(float(row["Pressure_Bottom"]))
                data["Humidity_Bottom"].append(float(row["Humidity_Bottom"]))
                data["Temperature_Bottom"].append(float(row["Temperature_Bottom"]))

                for i in range(1, 21):
                    data["CO2_main"][i - 1].append(float(row["CO2_main" + str(i)]))
                    data["Temperature_main"][i - 1].append(float(row["Temperature_main" + str(i)]))

                for i in range(1, 5):
                    data["CO2_side"][i - 1].append(float(row["CO2_side" + str(i)]))
                    data["Temperature_side"][i - 1].append(float(row["Temperature_side" + str(i)]))

    return data

def load_csv(path, limit = 100000):
    data = {
        "Timestamp": [],
        "Pressure_Top": [],
        "Humidity_Top": [],
        "Temperature_Top": [],
        "Pressure_Bottom": [],
        "Humidity_Bottom": [],
        "Temperature_Bottom": [],
        "CO2_main": [],
        "Temperature_main": [],
        "CO2_side": [],
        "Temperature_side": [],
    }

    for i in range(3, 3 + 20):
        data["CO2_main"].append([])
        data["Temperature_main"].append([])

    for i in range(3 + 20, 3 + 20 + 4):
        data["CO2_side"].append([])
        data["Temperature_side"].append([])

    with open(path, 'r', newline='') as csvfile:
        for index, row in enumerate(_csv_dict_reader(csvfile)):
            if index < limit:
                data["Timestamp"].append(float(row["Timestamp"]))
                data["Pressure_Top"].append(float(row["Pressure_Top"]))
                data["Humidity_Top"].append(float(row["Humidity_Top"]))
                data["Temperature_Top"].append(float(row["Temperature_Top"]))
                data["Pressure_Bottom"].append(float(row["Pressure_Bottom"]))
                data["Humidity_Bottom"].append(float(row["Humidity_Bottom"]))
                data["Temperature_Bottom"].append(float(row["Temperature_Bottom"]))

                co2_main = []
                temperature_main = []
                for i in range(1, 21):
                    data["CO2_main"][i - 1].append(float(row["CO2_main" + str(i)]))
                    data["Temperature_main"][i - 1].append(float(row["Temperature_main" + str(i)]))

                co2_side = []
                temperature_side = []
                for i in range(1, 5):
                    data["CO2_side"][i - 1].append(float(row["CO2_side" + str(i)]))
                    data["Temperature_side"][i - 1].append(float(row["Temperature_side" + str(i)]))
            else:
                return data

    return data

def load(path, limit = 100000):
    data = {
        "Timestamp": [],
        "Pressure_Top" : [],
        "Humidity_Top" : [],
        "Temperature_Top" : [],
        "Pressure_Bottom" : [],
        "Humidity_Bottom" : [],
        "Temperature_Bottom" : [],
        "CO2_main" : [],
        "Temperature_main" : [],
        "CO2_side" : [],
        "Temperature_side" : [],
    }

    for i in range(3, 3 + 20):
        data["CO2_main"].append([])
        data["Temperature_main"].append([])

    for i in range(3 + 20, 3 + 20 + 4):
        data["CO2_side"].append([])
        data["Temperature_side"].append([])

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

                data["Timestamp"].append(t)

                pressure, humidity, temperature = float(l[0]), float(l[1]), float(l[2])
                data["Pressure_Top"].append(pressure)
                data["Humidity_Top"].append(humidity)
                data["Temperature_Top"].append(temperature)

                pressure, humidity, temperature = float(l[3]), float(l[4]), float(l[5])
                data["Pressure_Bottom"].append(pressure)
                data["Humidity_Bottom"].append(humidity)
                data["Temperature_Bottom"].append(temperature)

                for i in range(3, 3 + 20):
                    co2 = float(l[2 * i])
                    temperature = float(l[2 * i + 1])
                    data["CO2_main"][i - 3].append(co2)
                    data["Temperature_main"][i - 3].append(temperature)

                for i in range(3 + 20, 3 + 20 + 4):
                    c02 = float(l[2 * i])
                    temperature = float(l[2 * i + 1])
                    data["CO2_side"][i - 20 - 3].append(c02)
                    data["Temperature_side"][i - 20 - 3].append(temperature)

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

# convert_txt_to_csv('data/1_CO2_raw_data/new_device_column1.txt', 'data/1_CO2_raw_data/data.csv')
# convert_txt_to_csv('data/1_CO2_raw_data/chunk_00.txt', 'data/1_CO2_raw_data/data.csv')

# convert_csv_to_bin('../data/1_CO2_raw_data/data.csv', '../data/1_CO2_raw_data/data.bin')