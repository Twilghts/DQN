import random
from heapq import heappush, heappop

import matplotlib.pyplot as plt
import networkx as nx


def k_shortest_paths(G, s, t, K):
    # G: weighted directed graph, with set of vertices V and set of directed edges E
    # s: source node
    # t: destination node
    # K: number of shortest paths to find
    # w(u, v): cost of directed edge from node u to node v (costs are non-negative)

    # Initialize the set of shortest paths P to be empty
    P = set()

    # Initialize the countu for all nodes u in the graph to be 0
    count = {u: 0 for u in G.nodes}

    # Initialize the heap B with the path Ps = {s} (a path consisting of just the source node s) with a cost of 0
    B = [(0, [s])]

    while B and count[t] < K:
        # Retrieve the path Pu with the lowest cost from the heap B
        C, Pu = heappop(B)

        # Increment countu for the destination node u of this path by 1
        u = Pu[-1]
        count[u] += 1

        if u == t:
            # If the destination node u of the path Pu is the destination node t, add Pu to the set of shortest paths P
            P.add(tuple(Pu))

        if count[u] <= K:
            # Iterate through each vertex v adjacent to u
            for v in G.neighbors(u):
                # Create a new path Pv by concatenating the edge (u, v) to the path Pu
                Pv = Pu + [v]

                # Insert this new path into the heap B with a cost equal to the cost of Pu plus the weight w(u, v) of the edge (u, v)
                heappush(B, (C + G.get_edge_data(u, v, default={'weight': 0})['weight'], Pv))

    # Return the set of shortest paths P
    return P


# Set the number of nodes and edges
n = 200
m = 10000
# Find the 3 shortest paths between node 1 and node 5
k = 3

# Generate the graph using the gnm_random_graph() function
G = nx.gnm_random_graph(n, m)
# Assign random weights to the edges
for u, v, d in G.edges(data=True):
    d['weight'] = random.randint(1, 100)

print(G.neighbors(12))
print([n for n in G.neighbors(12)])
print(G.get_edge_data(1, 11, default={'weight': 0})['weight'])

# Find the 3 shortest paths from s to t in the weighted directed graph G
P = k_shortest_paths(G, 1, 13, 10)
print(P)

# 可视化
# Add edge labels showing the weights\
# Draw the graph using the spring layout
# pos = nx.spring_layout(G)
# nx.draw(G, pos, with_labels=True)

# labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Show the plot
# plt.show()
