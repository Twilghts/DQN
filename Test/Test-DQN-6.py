import random
from collections import deque

import numpy as np
import tensorflow as tf

grid = [
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
]
ACTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class DQN:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(tf.keras.layers.Dense(24, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmin(act_values[0])  # returns action with minimum estimated steps

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amin(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target


import matplotlib.pyplot as plt


def visualize_path(agent, grid, start, goal):
    path = [start]
    current_state = start
    while any(current_state) != any(goal):
        action = agent.act(np.array([current_state]))
        next_state = current_state + np.array(ACTIONS)[action]
        path.append(next_state)
        current_state = next_state
    grid = np.array(grid)
    for point in path:
        grid[point[0], point[1]] = 5
    plt.imshow(grid, cmap='gray')
    plt.show()


dqn_agent = DQN(2, len(ACTIONS))
# train the agent
visualize_path(dqn_agent, grid, (0, 0), (4, 4))
