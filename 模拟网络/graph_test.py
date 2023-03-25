import matplotlib.pyplot as plt
import networkx as nx

from net import Net
from 利用network实现k最短路径算法 import k_shortest_paths

# G = nx.random_geometric_graph(20, 0.3)
# G = nx.grid_graph(dim=[5, 2])
# G = nx.watts_strogatz_graph(16, 4, 0.2)
# G = nx.barabasi_albert_graph(13, 2)
# relabel_table = {
#     number: int(number) for number in G.nodes
# }
# G = nx.relabel_nodes(G, relabel_table)
# nx.write_graphml(G, "graph.graphml")
G = nx.read_graphml("graph.graphml")
relabel_table = {
    number: int(number) for number in G.nodes
}
G = nx.relabel_nodes(G, relabel_table)
router_capacities = [919, 753, 883, 911, 1367, 552, 552, 1075, 1087, 1057, 633, 1141, 1080, 749, 1405, 856]
for u, v in G.edges:
    G[u][v]['weight']: int = (router_capacities[u] + router_capacities[v]) // 2
# 使用spring布局绘制图形
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)

# 添加显示权重的边标签
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# 显示绘图
plt.show()
net = Net()
for u, v in net.G.edges:
    print(f'边:{u}-{v},权值为:{net.G[u][v]["weight"]}')
print(k_shortest_paths(G, 0, 10, 4))
print(G[3].items())
print([s * 4 + a for s in G[3].keys() for a in range(4)])
