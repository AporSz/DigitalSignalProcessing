import csv
from .converters import CSV_FIELDNAMES

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

def get_data_by_minute(path):
    data = {
        "Timestamp": [], "Pressure_Top": [], "Humidity_Top": [], "Temperature_Top": [],
        "Pressure_Bottom": [], "Humidity_Bottom": [], "Temperature_Bottom": [],
        "CO2_main": [], "Temperature_main": [], "CO2_side": [], "Temperature_side": [],
    }
    for i in range(3, 3 + 20):
        data["CO2_main"].append([])
        data["Temperature_main"].append([])
    for i in range(3 + 20, 3 + 20 + 4):
        data["CO2_side"].append([])
        data["Temperature_side"].append([])

    with open(path, 'r') as csvfile:
        reader = _csv_dict_reader(csvfile)
        for index, row in enumerate(reader):
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

def load_csv(path, limit=100000):
    data = {
        "Timestamp": [], "Pressure_Top": [], "Humidity_Top": [], "Temperature_Top": [],
        "Pressure_Bottom": [], "Humidity_Bottom": [], "Temperature_Bottom": [],
        "CO2_main": [], "Temperature_main": [], "CO2_side": [], "Temperature_side": [],
    }
    for i in range(3, 3 + 20):
        data["CO2_main"].append([])
        data["Temperature_main"].append([])
    for i in range(3 + 20, 3 + 20 + 4):
        data["CO2_side"].append([])
        data["Temperature_side"].append([])

    with open(path, 'r') as csvfile:
        reader = _csv_dict_reader(csvfile)
        for index, row in enumerate(reader):
            if index < limit:
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
            else:
                return data
    return data

def load(path, limit=100000):
    data = {
        "Timestamp": [], "Pressure_Top": [], "Humidity_Top": [], "Temperature_Top": [],
        "Pressure_Bottom": [], "Humidity_Bottom": [], "Temperature_Bottom": [],
        "CO2_main": [], "Temperature_main": [], "CO2_side": [], "Temperature_side": [],
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
                if not line: break
                l = line.strip().split()
                if len(l) < 1: continue
                t = float(l[0])
                line = f.readline()
                if not line: break
                l = line.strip()[2:].split()
                if len(l) <= 2: continue

                data["Timestamp"].append(t)
                data["Pressure_Top"].append(float(l[0]))
                data["Humidity_Top"].append(float(l[1]))
                data["Temperature_Top"].append(float(l[2]))
                data["Pressure_Bottom"].append(float(l[3]))
                data["Humidity_Bottom"].append(float(l[4]))
                data["Temperature_Bottom"].append(float(l[5]))

                for i in range(3, 3 + 20):
                    data["CO2_main"][i - 3].append(float(l[2 * i]))
                    data["Temperature_main"][i - 3].append(float(l[2 * i + 1]))

                for i in range(3 + 20, 3 + 20 + 4):
                    data["CO2_side"][i - 20 - 3].append(float(l[2 * i]))
                    data["Temperature_side"][i - 20 - 3].append(float(l[2 * i + 1]))

                index += 1
            except Exception:
                pass
        return data
