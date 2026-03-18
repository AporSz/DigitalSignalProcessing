import numpy as np

# numbers = np.arange(0.5, 10.5, 0.5)
#
# print(np.sin(numbers))

readnumbers = np.array([])

with open("numbers.bin", "rb") as f:
    readnumbers = np.fromfile(f, np.float32)
    # print(readnumbers)

x = readnumbers[0::2]
y = readnumbers[1::2]
print(x)
print(y)