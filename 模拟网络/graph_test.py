import matplotlib.pyplot as plt
import networkx as nx

from net import Net

# G = nx.random_geometric_graph(20, 0.3)
# G = nx.grid_graph(dim=[5, 2])
G = nx.watts_strogatz_graph(16, 4, 0.2)
# G = nx.barabasi_albert_graph(13, 2)
relabel_table = {
    number: int(number) for number in G.nodes
}
G = nx.relabel_nodes(G, relabel_table)
# nx.write_graphml(G, "graph.graphml")
# G = nx.read_graphml("graph.graphml")
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
