import random

import numpy

from data import Data
from net import Net
from 模拟网络.DQN import DQN
from 模拟网络.利用network实现k最短路径算法 import k_shortest_paths


class DqnNetworkAgent(Net, DQN):
    def __init__(self):
        Net.__init__(self)
        DQN.__init__(self, state_size=1, action_size=len(self.G.nodes))
        self._k: int = 4  # k最短路径算法中路径的条数
        self.update_dataset()

    def k_shortest_paths_by_dqn(self, data):
        return k_shortest_paths(self.G, data.get_start(), data.get_goal(), self._k)

    def update_dataset(self, is_create_data=True):
        if is_create_data:
            data_number = random.randint(self.data_number_min, self.data_number_max)
            self.data_set: set = {Data(x, y, size=self.data_size) for x, y
                                  in
                                  zip(numpy.random.choice(self.G.nodes, data_number),
                                      numpy.random.choice(self.G.nodes, data_number)) if x != y}
            while len(self.data_set) < data_number:
                pair: tuple = random.sample(self.G.nodes, 2)
                self.data_set.add(Data(pair[0], pair[1], size=self.data_size))
            for data in self.data_set:
                paths = self.k_shortest_paths_by_dqn(data)
                data.shortest_path = self.choose_path(paths)
                self.routers[data.shortest_path[data.count]].put_receive_queue(data)
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
                self.routers[data.shortest_path[data.count]].put_receive_queue(data)
        """获取网络状态，存入DQN的回放缓存中，准备训练"""
        state = self.get_net_state()
        for item in state:
            reword = - (item[1][0] + item[1][1])
            net_state = 0  # 默认不忙碌
            if 0.45 < item[1][0] <= 0.66:
                net_state = 1  # 最低级别忙碌
            elif 0.66 < item[1][0] <= 0.9:
                net_state = 2  # 次高级别忙碌
            else:
                net_state = 3  # 最高级别忙碌
