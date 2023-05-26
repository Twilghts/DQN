import random

import numpy
from 网络基础构件.net import Net
from 网络基础构件.package import Package
from DQN import DQN
from K最短路径算法 import k_shortest_paths


class DqnNetworkAgent(Net, DQN):
    def __init__(self):
        Net.__init__(self)
        DQN.__init__(self, state_size=1, action_size=len(self.G.nodes))
        self._k: int = 3  # k最短路径算法中路径的条数
        self.packet_for_train = set()

    def k_shortest_paths_by_dqn(self, data):
        return k_shortest_paths(self.G, data.get_start(), data.get_goal(), self._k)

    def update_dataset(self, is_create_data=True, is_best=False):
        if is_create_data:
            data_number = random.randint(self.data_number_min, self.data_number_max)
            self.data_set: set = {Package(x, y, size=self.data_size) for x, y
                                  in
                                  zip(numpy.random.choice(self.G.nodes, self.data_number),
                                      numpy.random.choice(self.G.nodes, self.data_number)) if x != y}
            while len(self.data_set) < self.data_number:
                pair: tuple = random.sample(self.G.nodes, 2)
                self.data_set.add(Package(pair[0], pair[1], size=self.data_size))
            for data in self.data_set:
                if self.routers[data.get_start()].datasize - self.routers[data.get_start()].cache >= data.size:
                    self.total_data_number += 1
                    paths = self.k_shortest_paths_by_dqn(data)
                    data.shortest_path = self.choose_path(paths, is_best=is_best)
                    self.routers[data.shortest_path[data.count]].put_receive_queue(data)
        """获取网络状态，将数据存入DQN的回放缓存中，准备训练"""
        """转发每个路由器中队首的数据包，放入链路中"""
        for router in self.routers.values():
            data = router.pop_send_queue()  # 如果队列为空的话返回空值
            if data is not None:
                router_now_sign = data.shortest_path[data.count]
                router_next_sign = data.shortest_path[data.count + 1]
                link = (router_now_sign, router_next_sign)
                if link not in self.links.keys():
                    link = (router_next_sign, router_now_sign)
                self.links[link].put_data(data)
                data.count += 1
        """将链路中的数据包转发到路由器上"""
        for link in self.links.values():
            data = link.pop_data()
            if data is not None:
                is_success_or_over = self.routers[data.shortest_path[data.count]].put_receive_queue(data,
                                                                                                    old_state=
                                                                                                    data.shortest_path[
                                                                                                        data.count - 1])
                if is_success_or_over[0]:
                    self.success_data_number += 1
                if is_success_or_over[1]:
                    self.packet_for_train.add(data)
                    self.packet_for_record.add(data)
