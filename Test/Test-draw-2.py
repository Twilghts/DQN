import matplotlib.pyplot as plt
import numpy as np

# Create an array of zeros with shape (300, 300) and data type float
img = np.zeros((300, 300), dtype=np.float32)

# Set the value of the middle row to 1
img[150, :] = 1

# Plot the image using imshow
plt.imshow(img, cmap='gray')

# Show the plot
plt.show()
