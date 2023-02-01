import matplotlib.pyplot as plt
import networkx as nx

# Create an empty graph with no nodes and no edges
G = nx.Graph()

# Add three nodes to the graph
G.add_node(1)
G.add_node(2)
G.add_node(3)

# Add an edge between nodes 1 and 2, and another edge between nodes 2 and 3
G.add_edge(1, 2)
G.add_edge(2, 3)

# Draw the graph using the spring layout
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)

# Show the plot
plt.show()
