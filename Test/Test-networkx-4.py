import networkx as nx

# Create a weighted undirected graph
G = nx.Graph()
G.add_edge('A', 'B', weight=1)
G.add_edge('B', 'C', weight=2)
G.add_edge('C', 'D', weight=3)
G.add_edge('A', 'D', weight=4)

# Compute the 2 shortest paths from source node 'A' to _target node 'D'
k = 2
paths = list(nx.all_shortest_paths(G, 'A', 'D', weight='weight'))[:k]

# Print the paths
for i, p in enumerate(paths):
    print(f"Path {i}: {p}")
