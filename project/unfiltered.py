import numpy as np

def load(path):
    data = []
    with open(path) as f:
        for line in f:
            l = line.strip().split()
            t = float(l[0])
            

            print(l)

    return None

data = load('data/1_CO2_raw_data/new_device_column1.txt')