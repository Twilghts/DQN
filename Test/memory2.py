# Set the number of nodes and edges
# n = 20  # 点的数量
# m = 100  # 边的数量
# # Find the 3 shortest paths between node 1 and node 5
# k = 10  # 最短路径的数量
# start_time = time.perf_counter()
# # Generate the graph using the gnm_random_graph() function
# G = nx.gnm_random_graph(n, m)
# # Assign random weights to the edges
# for u, v, d in G.edges(transfer_package=True):
#     d['weight'] = random.randint(1, 100)
#
# # Graph = {u: [] for u in G.nodes}
# # for i in G.nodes:
# #     for j in range(len(G)):
# #         Graph[i].append((j, -G.get_edge_data(i, j, default={'weight': 1000})['weight']))
# # print([n for n in G.neighbors(12)])
# # print(G.get_edge_data(1, 11, default={'weight': 0})['weight'])
# # print(Graph)
#
# # Find the 3 shortest paths from s to t in the weighted directed graph G
# P = k_shortest_paths(G, 1, 13, k)
# print(P)
# print(f"消耗时间:{time.perf_counter() - start_time}")
#
# # 可视化
# # Add edge labels showing the weights\
# # Draw the graph using the spring layout
# pos = nx.spring_layout(G)
# nx.draw(G, pos, with_labels=True)
# #
# labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
#
# # Show the plot
# plt.show()
