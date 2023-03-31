import random
import time

import matplotlib.pyplot as plt
import networkx as nx

from link import Link
from router import Router


class Net:
    def __init__(self):
        self.total_data_number = 0
        self.success_data_number = 0
        self.data_number_min = 300
        self.data_number_max = 700
        self.data_number = 400
        self.G = nx.read_graphml("graph.graphml")
        """读取出来的图的节点是字符串类型的，离谱！要更改节点的名字"""
        relabel_table = {
            number: int(number) for number in self.G.nodes
        }
        self.G = nx.relabel_nodes(self.G, relabel_table)
        self.router_capacities = [919, 753, 883, 911, 1367, 552, 552, 1075, 1087, 1057, 633, 1141, 1080, 749, 1405, 856]
        """路由器组 为字典，键为路由器的编号，值为所对应的路由器,设置路由器内部可存储的数据容量。"""
        self.routers: dict = {
            number: Router(number, datasize=self.router_capacities[number]) for number in self.G.nodes
        }
        """更新图的边权值， 为其两头路由器容量之和的一半"""
        for u, v in self.G.edges:
            self.G[u][v]['weight']: int = (self.routers[u].datasize + self.routers[v].datasize) // 2
        """网络连接组 为字典，键为起始路由器和终止路由器的元组，值为相对应的网络链接。"""
        self.links: dict = {
            (start, target): Link((start, target), delay=0.001) for start, target in self.G.edges
        }
        """数据包集合，一共有指定数目个数据包,每个数据包的大小都不同。"""
        self.data_size: int = 10  # 数据包的大小
        """本数据集合用于充当背景环境。"""
        self.data_set: set = set()
        """信息流的记录信息,键为数据包本体，值为数据包在网络中传输的记录, 为DQN训练做准备"""
        self.logs: dict = {
            data: [] for data in self.data_set
        }
        self.time: float = 0  # 网络开始传输信息时的时间戳，传输过程中用于计算吞吐量，传输结束后用于计算总传播时间。
        self.packet_for_record = set()

    """返回路由器组的网络状态，格式为以路由器序号为key，r1的缓存/r1的容量为value"""

    def get_net_state(self) -> dict:
        return {
            router.sign: (router.cache / router.datasize, self.calculate_loss(router.sign)) for router in
            self.routers.values()
        }
    """专门计算丢包率的函数，之前没想到数据包数量不够，经过一个路由器的数据包数量会是0"""
    def calculate_loss(self, number):
        router = self.routers[number]
        if router.total != 0:
            return router.failure / router.total
        else:
            return 0

    def update_dataset(self):
        """更新数据包内容。一部分是用于dqn训练，另一部分当作背景环境。此函数由子类重写
        """

    def show_graph(self):
        # 使用spring布局绘制图形
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True)

        # 添加显示权重的边标签
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)

        # 显示绘图
        plt.show()

    def calculate_handling_capacity(self, router_sign, handling_capacity):
        if len(self.routers[router_sign].handling_capacity) == 0:
            self.routers[router_sign].handling_capacity.append(
                (round(time.perf_counter() - self.time, 4), handling_capacity))
        else:
            """基础数值等于路由器最后状态([-1])的吞吐量([1])"""
            base_value = self.routers[router_sign].handling_capacity[-1][1]
            new_value = base_value + handling_capacity
            self.routers[router_sign].handling_capacity.append((round(time.perf_counter() - self.time, 4), new_value))
