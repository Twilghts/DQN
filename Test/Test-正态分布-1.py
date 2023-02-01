import matplotlib.pyplot as plt
import numpy as np

# Set the range of x
x = np.linspace(-3, 3, 100)

# Calculate the PDF of standard normal distribution
y = (1 / np.sqrt(2 * np.pi)) * np.exp(-x ** 2 / 2)

# Plot the PDF
plt.plot(x, y)

# Show the plot
plt.show()
