import random
import collections

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

deque = collections.deque(maxlen=100)
print(deque.pop())