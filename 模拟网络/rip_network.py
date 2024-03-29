import random

import networkx as nx
import numpy

from package import Data
from net import Net


class Rip(Net):
    def __init__(self):
        super().__init__()
        for u, v in self.G.edges:
            self.G[u][v]['weight']: float = 1
        """构建每一个路由器的路由表"""
        for _router in self.routers.values():
            _router.routing_table = {
                node: nx.dijkstra_path(self.G, _router.sign, node) for node in self.G.nodes
            }

    def update_dataset(self, is_create_data=True):
        """如果选择创建数据包，就创建并转发数据包"""
        if is_create_data:
            # data_number = random.randint(self.data_number_min, self.data_number_max)
            self.data_set: set = {Data(x, y, size=self.data_size) for x, y
                                  in
                                  zip(numpy.random.choice(self.G.nodes, self.data_number),
                                      numpy.random.choice(self.G.nodes, self.data_number)) if x != y}
            while len(self.data_set) < self.data_number:
                pair: tuple = random.sample(self.G.nodes, 2)
                self.data_set.add(Data(pair[0], pair[1], size=self.data_size))
            for data in self.data_set:
                if self.routers[data.get_start()].datasize - self.routers[data.get_start()].cache >= data.size:
                    data.shortest_path = nx.dijkstra_path(self.G, data.get_start(), data.get_goal())
                    self.routers[data.shortest_path[data.count]].put_receive_queue(data, is_rip=True)
                    self.total_data_number += 1
        """转发每个路由器中队首的数据包，放入链路中"""
        for router in self.routers.values():
            data = router.pop_send_queue()
            if data is not None:
                link = (data.shortest_path[data.count], data.shortest_path[data.count + 1])
                if link not in self.links.keys():
                    link = (data.shortest_path[data.count + 1], data.shortest_path[data.count])
                self.links[link].put_data(data)
                data.count += 1
        """将链路中的数据包转发到路由器上"""
        for link in self.links.values():
            data = link.pop_data()
            if data is not None:
                is_success_or_over = self.routers[data.shortest_path[data.count]].put_receive_queue(data,
                old_state=data.shortest_path[data.count - 1], is_rip=True)
                if is_success_or_over[0]:
                    self.success_data_number += 1
                if is_success_or_over[1]:
                    self.packet_for_record.add(data)
