import copy
import random

import networkx as nx
import numpy

from package import Data
from net import Net


class Ospf(Net):
    def __init__(self):
        super().__init__()
        self.dynamic_graph = copy.deepcopy(self.G)  # 创建一个副本图，用于体现Ospf的动态性。

    """在传输信息的同时对网络进行动态更新"""

    def update_graph(self):
        """对每一个路由器进行访问，对连接不同繁忙级别的路由器的链路设置不同的权值"""
        modificate_edges: set = set()  # 统计所有被修改过的边。
        for router in self.routers.values():
            """最低级别繁忙。"""
            if 0.45 < router.cache / router.datasize <= 0.60:
                """获取直接与该节点相接的链路。"""
                edges: set = {(u, v) for u, v in self.dynamic_graph.edges if u == router.sign or v == router.sign}
                """修改每一条链路的权值。edge为元组"""
                for edge in edges:
                    self.dynamic_graph[edge[0]][edge[1]]['weight'] = 1500
                modificate_edges |= edges  # 两个集合做并集。不会有重复元素。
            elif 0.60 < router.cache / router.datasize <= 0.75:
                """次高级别繁忙"""
                """获取直接与该节点相接的链路。"""
                edges: set = {(u, v) for u, v in self.dynamic_graph.edges if u == router.sign or v == router.sign}
                """修改每一条链路的权值。edge为元组"""
                for edge in edges:
                    self.dynamic_graph[edge[0]][edge[1]]['weight'] = 2500
                modificate_edges |= edges  # 两个集合做并集。不会有重复元素。
            elif router.cache / router.datasize > 0.75:
                """最高级别繁忙"""
                """获取直接与该节点相接的链路。"""
                edges: set = {(u, v) for u, v in self.dynamic_graph.edges if u == router.sign or v == router.sign}
                """修改每一条链路的权值。edge为元组"""
                for edge in edges:
                    self.dynamic_graph[edge[0]][edge[1]]['weight'] = 4000
                modificate_edges |= edges  # 两个集合做并集。不会有重复元素。
        """获取所有未经修改的边。"""
        dismodificate_edges: set = {(u, v) for u, v in self.dynamic_graph.edges if (u, v) not in modificate_edges}
        """将未修改的边的权值恢复"""
        for u, v in dismodificate_edges:
            self.dynamic_graph[u][v]['weight'] = self.G[u][v]['weight']

    """每次结束一整次传输信息时，对图进行全局复原。"""

    def retry_graph(self):
        self.dynamic_graph = copy.deepcopy(self.G)

    def update_dataset(self, is_create_data=True):
        if is_create_data:
            data_number = random.randint(self.data_number_min, self.data_number_max)
            self.data_set: set = {Data(x, y, size=self.data_size) for x, y
                                  in
                                  zip(numpy.random.choice(self.G.nodes, self.data_number),
                                      numpy.random.choice(self.G.nodes, self.data_number)) if x != y}
            while len(self.data_set) < self.data_number:
                pair: tuple = random.sample(self.G.nodes, 2)
                self.data_set.add(Data(pair[0], pair[1], size=self.data_size))
            for data in self.data_set:
                """当路由器有容量的时候才放数据包"""
                if self.routers[data.get_start()].datasize - self.routers[data.get_start()].cache >= data.size:
                    data.shortest_path = nx.dijkstra_path(self.dynamic_graph, data.get_start(), data.get_goal())
                    self.routers[data.shortest_path[0]].put_receive_queue(data)  # 将数据包放入起始路由器中
                    self.total_data_number += 1
        self.update_graph()  # 更新网络状态
        """转发每个路由器中队首的数据包，放入链路中"""
        for router in self.routers.values():
            data = router.pop_send_queue()
            if data is not None:
                data.shortest_path = nx.dijkstra_path(self.dynamic_graph, router.sign, data.get_goal())
                link = (data.shortest_path[0], data.shortest_path[1])
                if link not in self.links.keys():
                    link = (data.shortest_path[1], data.shortest_path[0])
                self.links[link].put_data(data)
        """将链路中的数据包转发到路由器上"""
        for link in self.links.values():
            data = link.pop_data()
            if data is not None:
                is_success_or_over = self.routers[data.shortest_path[1]].put_receive_queue(data,
                old_state=data.shortest_path[data.count - 1])
                if is_success_or_over[0]:
                    self.success_data_number += 1
                if is_success_or_over[1]:
                    self.packet_for_record.add(data)
