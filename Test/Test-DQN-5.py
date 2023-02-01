import random

import networkx as nx
import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam
import time

# # Create the graph using NetworkX
# G = nx.Graph()
# G.add_weighted_edges_from(
#     [(0, 1, 50), (0, 2, 21), (1, 3, 4), (1, 4, 32), (2, 5, 100), (3, 6, 21), (4, 6, 9), (5, 6, 58), ()])
# Set the number of nodes and edges
n = 10
m = 40
# Find the 3 shortest paths between node 1 and node 5
k = 10

start_time = time.perf_counter()
# Generate the graph using the gnm_random_graph() function
G = nx.gnm_random_graph(n, m)
# Assign random weights to the edges
for u, v, d in G.edges(data=True):
    d['weight'] = random.randint(1, 100)

# Define the destination node
destination = 6

# Define the Q-network
model = Sequential()
model.add(Dense(64, input_dim=1, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(len(G.nodes), activation='linear'))
model.compile(loss='mse', optimizer=Adam())

# Training
for episode in range(1000):
    # Start at a random node
    current_state = random.choice(list(G.nodes))

    while current_state != destination:
        # Select an action
        q_values = model.predict(np.array([current_state]))
        action = np.argmin([G[current_state][node]['weight'] for node in G[current_state]])

        # Take the action
        next_state = list(G[current_state])[action]
        reward = G[current_state][next_state]['weight']

        # Update the Q-value for the current state
        q_values[0][action] = reward + np.min(model.predict(np.array([next_state]))[0])
        model.fit(np.array([current_state]), q_values, verbose=0)

        current_state = next_state

# Testing
current_state = 0
path = [current_state]
while current_state != destination:
    q_values = model.predict(np.array([current_state]))
    action = np.argmin([G[current_state][node]['weight'] for node in G[current_state]])
    current_state = list(G[current_state])[action]
    path.append(current_state)
print("Shortest path:", path)
