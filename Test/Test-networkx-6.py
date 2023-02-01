# Set the number of nodes and edges
import random
import time

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import tensorflow as tf

n = 5
m = 20
# Find the 3 shortest paths between node 1 and node 5
k = 10

start_time = time.perf_counter()
# Generate the graph using the gnm_random_graph() function
G = nx.gnm_random_graph(n, m)
# Assign random weights to the edges
for u, v, d in G.edges(data=True):
    d['weight'] = random.randint(1, 100)
# print(G[4].items())
print([(next_s, a) for next_s, a in G[4].items()])
print(np.array([7]))
# print(G[1][7])

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(24, input_dim=1, activation='relu'))
model.add(tf.keras.layers.Dense(24, activation='relu'))
model.add(tf.keras.layers.Dense(len(G.nodes), activation='linear'))
model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))

# print([model.predict(np.array([next_s]))[0][a['weight']] for next_s, a in G[2].items()])
print(model.predict(np.array([6])))
# print(model.predict([4])[0][5])
# print(model.predict(4)[0][5])
# Draw the graph using the spring layout
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)

# Add edge labels showing the weights
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Show the plot
plt.show()
