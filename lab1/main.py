x = 5

lst = [9, x, [2, 3], lambda x: x**2]

# print(lst[1])
# print(lst[4])
# print(lst[-1])
# print(lst[-2])
# print(lst[-5])
# print(lst[2:4])
# print(lst[:2])
# print(lst[2:])
# print(lst[:-1])
# print(lst[2:2])
# print(lst[:])
# print(lst[0:0])

import matplotlib.pyplot as plt
import numpy as np

x = [0, 1]
y = [1, 2]

# fig, ax = plt.subplots()
#plt.plot(x,y)

# plt.plot(x,y,'.')

# plt.plot(x,y,'-o')

plt.plot(x,y,'-o', linewidth=13,markersize=20,label='myline')

plt.legend()
plt.show()
