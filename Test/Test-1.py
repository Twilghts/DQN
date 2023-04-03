import numpy as np

value = 0
for i in range(1, 1700):
    value += np.log10((2 * i + 1) / i)
print(value)