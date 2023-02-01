import time

from 模拟网络.DQN import DQN
from 模拟网络.利用network实现k最短路径算法 import k_shortest_paths
from net import Net


class DqnNetworkAgent(Net, DQN):
    def __init__(self):
        Net.__init__(self)
        DQN.__init__(self, state_size=1, action_size=len(self.G.nodes))
        self._k = 4  # k最短路径算法中路径的条数

    def k_shortest_paths_by_dqn(self, data):
        return k_shortest_paths(self.G, data.get_start(), data.get_goal(), self._k)


if __name__ == '__main__':
    start_time = time.perf_counter()
    dqn_net = DqnNetworkAgent()
    # for router in dqn_net.routers:
    #     print(f'路由器序号:{router.sign},对应的路由表:{router.routing_table}')
    print(dqn_net.routers)
    print(dqn_net.links)
    print(dqn_net.data_set)
    print(f'消耗时间:{time.perf_counter() - start_time}')
