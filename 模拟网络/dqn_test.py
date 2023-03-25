import time

import numpy as np

from DQN import DQN

agent = DQN(2, 10)

print(agent.model(np.array([[0, 1], [1, 0]])).numpy())
print(agent.model(np.array([[0, 1], [1, 1]])).numpy())
print(agent.model(np.array([[1, 0], [1, 1]])).numpy())
print(agent.model(np.array([[3, 8], [1, 2]])).numpy())
n1 = np.array([[2, 3, 1]])
print(n1)
n2 = np.array([1, 2, 3])
n3 = np.array([[1, 2], [2, 1]])
time.sleep(1)