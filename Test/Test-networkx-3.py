import random

import matplotlib.pyplot as plt
import networkx as nx

# Set the number of nodes and edges
n = 20
m = 50

# Generate the graph using the gnm_random_graph() function
G = nx.gnm_random_graph(n, m)

# Assign random weights to the edges
for u, v, d in G.edges(data=True):
    d['weight'] = random.randint(1, 100)

# Draw the graph using the spring layout
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)

# Add edge labels showing the weights
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Show the plot
plt.show()
