import matplotlib.pyplot as plt

x1 = [1, 2, 3, 4, 5]
y1 = [2, 4, 6, 8, 10]

x2 = [2, 4, 6, 8, 10]
y2 = [1, 2, 4, 8, 16]

plt.plot(x1, y1, label='Line 1')
plt.plot(x2, y2, label='Line 2')

plt.xlabel('X-axis')
plt.ylabel('Y-axis')

plt.title('Multiple Line Charts')

plt.legend()
plt.show()
