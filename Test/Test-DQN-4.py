import random
from collections import defaultdict

import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam

# Define the graph
graph = defaultdict(list)
graph[0] = [(1, 5), (2, 2)]
graph[1] = [(3, 1), (4, 8)]
graph[2] = [(5, 10)]
graph[3] = [(6, 2)]
graph[4] = [(6, 3)]
graph[5] = [(6, 5)]

# Define the destination node
destination = 6

# Define the Q-network
model = Sequential()
model.add(Dense(64, input_dim=1, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(len(graph[0]), activation='linear'))
model.compile(loss='mse', optimizer=Adam())

# Training
for episode in range(1000):
    # Start at a random node
    current_state = random.randint(0, len(graph) - 1)

    while current_state != destination:
        # Select an action
        q_values = model.predict(np.array([current_state]))
        action = np.argmin([edge[1] for edge in graph[current_state]])

        # Take the action
        next_state, reward = graph[current_state][action]

        # Update the Q-value for the current state
        q_values[0][action] = reward + np.min(model.predict(np.array([next_state]))[0])
        model.fit(np.array([current_state]), q_values, verbose=0)

        current_state = next_state

# Testing
current_state = 0
path = [current_state]
while current_state != destination:
    q_values = model.predict(np.array([current_state]))
    action = np.argmin([edge[1] for edge in graph[current_state]])
    current_state, _ = graph[current_state][action]
    path.append(current_state)
print("Shortest path:", path)
