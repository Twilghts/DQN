import networkx as nx

# Create an empty graph with no nodes and no edges
G = nx.Graph()

# Add three nodes to the graph
G.add_node(1)
G.add_node(2)
G.add_node(3)

# Add an edge between nodes 1 and 2
G.add_edge(1, 2)

# Print the number of nodes and edges in the graph
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")

# Print the nodes and edges in the graph
print(f"Nodes: {G.nodes()}")
print(f"Edges: {G.edges()}")

# Remove the edge between nodes 1 and 2
G.remove_edge(1, 2)

# Print the number of nodes and edges in the graph
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")
print(nx.__version__)
