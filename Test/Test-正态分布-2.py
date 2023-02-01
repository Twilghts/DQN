import math

import matplotlib.pyplot as plt
import numpy as np

# Set the range of x
x = np.linspace(-3, 3, 100)

# Calculate the distribution function of standard normal distribution
y = (1 / 2) * (1 + math.erf(x / np.sqrt(2)))

# Plot the distribution function
plt.plot(x, y)

# Show the plot
plt.show()
