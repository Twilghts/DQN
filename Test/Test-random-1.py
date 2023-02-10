import random

import numpy

numbers = [1, 2, 3, 4, 5]
random_numbers = random.sample(numbers, 3)
print(random_numbers)
print(numpy.mean(random_numbers))
