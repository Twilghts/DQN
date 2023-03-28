import random
from collections import deque
from queue import Queue

import numpy as np


# angle_in_radians = math.pi / 4  # Example angle in radians
# sin_value = math.sin(angle_in_radians)
#
# print(sin_value)  # Output: 0.7071067811865475
#
# print([math.sin(n) for n in range(40)])


def normal_uniform(u, sigma, n):
    # Generate normally distributed numbers
    normal_numbers = np.random.normal(u, sigma, 10000)

    # Select n indices randomly
    indices = random.sample(range(len(normal_numbers)), n)

    # Compute uniformly distributed numbers in the range u-sigma to u+sigma
    uniform_numbers = [int(random.uniform(u - 3 * sigma, u + 3 * sigma)) for i in indices]

    return uniform_numbers


print(normal_uniform(1000, 150, 16))

print(all([1, 1, 1, 1, 1, 1]))
print(any([0, 0, 0, 0]))
print(7 // 4)
for step in range(30, 100, 10):
    print(step)
q_1 = deque(maxlen=10)
for i in range(15):
    q_1.append(i)
minibatch = random.sample(q_1, 3)
print(minibatch)
print(q_1)

