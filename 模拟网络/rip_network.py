import time

import matplotlib.pyplot as plt
import networkx as nx

from net import Net


class Rip(Net):
    def __init__(self):
        super().__init__()
        for u, v in self.G.edges:
            self.G[u][v]['weight'] = 1
        """构建每一个路由器的路由表"""
        for _router in self.routers.values():
            _router.routing_table = {
                node: nx.dijkstra_path(self.G, _router.sign, node) for node in self.G.nodes
            }


if __name__ == '__main__':
    start_time = time.perf_counter()
    rip_net = Rip()
    # for router in rip_net.routers:
    #     print(f'路由器序号:{router.sign},对应的路由表:{router.routing_table}')
    print(rip_net.routers)
    print('*' * 200)
    print(rip_net.links)
    print('*' * 200)
    print(rip_net.data_set)
    # 使用spring布局绘制图形
    pos = nx.spring_layout(rip_net.G)
    nx.draw(rip_net.G, pos, with_labels=True)

    # 添加显示权重的边标签
    labels = nx.get_edge_attributes(rip_net.G, 'weight')
    nx.draw_networkx_edge_labels(rip_net.G, pos, edge_labels=labels)

    # 显示绘图
    plt.show()
    print(f'消耗时间为{time.perf_counter() - start_time}')
