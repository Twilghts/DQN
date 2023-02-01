# # Set the number of nodes and edges
# import random
#
# import networkx as nx
#
import time
import random
from 模拟网络.link import Link
n = 500  # 点的数量
m = 1500  # 边的数量
# _start = 1  # 起始点
# _target = 10  # 目标点
#
import networkx as nx

start_time = time.perf_counter()
G = nx.gnm_random_graph(n, m)
# Assign random weights to the edges
for u, v, d in G.edges(data=True):
    d['weight'] = random.randint(1, 100)
#
# import matplotlib.pyplot as plt
# import networkx as nx
#
# G = nx.Graph()
# G.add_weighted_edges_from([(0, 1, 30), (0, 2, 45), (1, 2, 40), (1, 3, 10),
#                            (2, 5, 20), (3, 4, 70), (4, 5, 25), (5, 7, 15),
#                            (4, 8, 30), (7, 8, 20), (6, 7, 5), (6, 10, 20),
#                            (8, 9, 15), (9, 10, 5)])
# # Draw the graph using the spring layout
# pos = nx.spring_layout(G)
# nx.draw(G, pos, with_labels=True)
# #
# labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
#
# # Show the plot
# plt.show()

# Find the shortest path
# state = _start
# path = [_start]
# while state != goal:
#     action = dqn_agent.act(state, G)
#     path.append(action)
#     state = action
links = [Link((start, target), delay=weight['weight']) for start, target, weight in G.edges(data=True)]
print(links)
print(f'消耗时间:{time.perf_counter() - start_time}')