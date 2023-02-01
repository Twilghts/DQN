# for n in range(10):
#     print(random.choice(range(3, 20, 3)))

# Set the number of nodes and edges
n = 8
m = 16
# Find the 3 shortest paths between node 1 and node 5
k = 10

# Generate the graph using the gnm_random_graph() function
# G = nx.gnm_random_graph(n, m)
# print([n for n in G.neighbors(5)])
# for n in range(10):
#     print(random.choice([n for n in G.neighbors(5)]))
# print('*' * 100)
# tuple_1 = (1, 2)
# print(tuple_1[0])
# G = nx.Graph()
# G.add_weighted_edges_from([(0, 1, 30), (0, 2, 45), (1, 2, 40), (1, 3, 10),
#                            (2, 5, 20), (3, 4, 70), (4, 5, 25), (5, 7, 15),
#                            (4, 8, 30), (7, 8, 20), (6, 7, 5), (6, 10, 20),
#                            (8, 9, 15), (9, 10, 5)])
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
# start = 1
# goal = 6
# _k = 3  # k最短路径的总数
# P = K最短路径.利用network实现k最短路径算法.k_shortest_paths(G, start, goal, _k)
# dqn_agent = DQN(1, len(G.nodes()))
#
# values = {}
# for _path in P:
#     value = random.randint(0, 10)
#     values[value] = _path
#     print(value)
# path = max([_item for _item in values.items()],
#            key=lambda x: x[0])[1]
# print([_item[0] for _item in values.items()])
# print(values.keys())
# print(P)
# print(path)
# print(dqn_agent.model.predict(np.array([7])))
# print(dqn_agent.model(np.array([7])))
# predict = dqn_agent.model(np.array([7])).numpy()
# predict[0][8] = 20
# print(predict)
# dqn_agent.model.fit(np.array([7]), predict, epochs=1, verbose=0)
# print(dqn_agent.model.predict(np.array([7])))
# print(dqn_agent.model(np.array([7])))
