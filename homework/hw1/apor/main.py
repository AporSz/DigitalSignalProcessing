## 2. Write a Python script without using explicit loops that performs the following:

## (a) Generate an array with values {0.5, 1, 1.5, 2, 2.5, 3, . . . , 8.5, 9, 9.5, 10} using the numpy.arange function.

import numpy as np

numbers = np.arange(0.5, 10.5, 0.5)

#print(numbers)

## (b) Write to a text file in two columns the array and the sine of each value (use the sin function).

with open("numbers.txt", "w") as f:
    sins = np.sin(numbers)
    outnumbers = np.column_stack((numbers, sins))
    np.savetxt(f, outnumbers)

## (c) Repeat the above task using binary file in 32-bit float format.

with open("numbers.bin", "wb") as f:
    numbers32 = outnumbers.astype(np.float32)
    numbers32.tofile(f)

## 3. Write another Python script without using loops that performs the following:

## (a) Reads in the previously written array from the binary file.

readnumbers = np.array([])

with open("numbers.bin", "rb") as f:
    readnumbers = np.fromfile(f, np.float32)
    print(readnumbers)

## (b) Plots the sine curve. The axes should be labeled. Grid, legend and title should be applied

import matplotlib.pyplot as plt

x = readnumbers[0::2]
y = readnumbers[1::2]

plt.plot(x, y, ".-", )
plt.xlabel("x")
plt.ylabel("y")
plt.legend(["sin(x)"])
plt.title("Plot of x and y")
plt.grid()

#plt.show()

## (c) Saves the figure.

plt.savefig("plot.png")