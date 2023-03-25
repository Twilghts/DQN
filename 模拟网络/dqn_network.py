import random

import numpy

from data import Data
from net import Net
from 模拟网络.DQN import DQN
from 模拟网络.利用network实现k最短路径算法 import k_shortest_paths


class DqnNetworkAgent(Net, DQN):
    def __init__(self):
        Net.__init__(self)
        DQN.__init__(self, state_size=1, action_size=len(self.G.nodes) * 4)
        self._k: int = 3  # k最短路径算法中路径的条数
        self.update_dataset()

    def k_shortest_paths_by_dqn(self, data):
        return k_shortest_paths(self.G, data.get_start(), data.get_goal(), self._k)

    def update_dataset(self, is_create_data=True):
        if is_create_data:
            state = self.get_net_state()  # 根据网络环境的状态选择路径(action)
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
                data.shortest_path = self.choose_path(paths, state)
                self.routers[data.shortest_path[data.count]].put_receive_queue(data)
        """获取网络状态，将数据存入DQN的回放缓存中，准备训练"""
        state = self.get_net_state()
        preprocessing = {
            number: () for number in state.keys()
        }  # 针对DQN训练的预处理数据
        for item in state.items():
            reword = - (item[1][0] + item[1][1])  # -（路由器缓存/路由器容量 + 丢包率）
            net_state = 0  # 默认不忙碌
            if 0.45 < item[1][0] <= 0.66:
                net_state = 1  # 最低级别忙碌
            elif 0.66 < item[1][0] <= 0.9:
                net_state = 2  # 次高级别忙碌
            elif item[1][0] > 0.9:
                net_state = 3  # 最高级别忙碌
            preprocessing[item[0]] = (reword, net_state)
        """转发每个路由器中队首的数据包，放入链路中"""
        for router in self.routers.values():
            data = router.pop_send_queue()  # 如果队列为空的话返回空值
            if data is not None:
                router_now_sign = data.shortest_path[data.count]
                router_next_sign = data.shortest_path[data.count + 1]
                """为DQN训练做准备"""
                dqn_now_state = router_now_sign * 4 + preprocessing[router_now_sign][1]
                dqn_next_state = router_next_sign * 4 + preprocessing[router_next_sign][1]
                dqn_now_reword = preprocessing[router_now_sign][0] + preprocessing[router_next_sign][0]
                self.remember(dqn_now_state, dqn_next_state, dqn_now_reword, dqn_next_state, False)
                link = (router_now_sign, router_next_sign)
                if link not in self.links.keys():
                    link = (router_next_sign, router_now_sign)
                self.links[link].put_data(data)
                data.count += 1
        """将链路中的数据包转发到路由器上"""
        for link in self.links.values():
            data = link.pop_data()
            if data is not None:
                self.routers[data.shortest_path[data.count]].put_receive_queue(data)