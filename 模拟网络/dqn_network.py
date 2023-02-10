from net import Net
from 模拟网络.DQN import DQN
from 模拟网络.利用network实现k最短路径算法 import k_shortest_paths


class DqnNetworkAgent(Net, DQN):
    def __init__(self):
        Net.__init__(self)
        DQN.__init__(self, state_size=1, action_size=len(self.G.nodes))
        self._k: int = 4  # k最短路径算法中路径的条数

    def k_shortest_paths_by_dqn(self, data):
        return k_shortest_paths(self.G, data.get_start(), data.get_goal(), self._k)

    def send_message(self, data, is_dqn=True, path=None):
        """如果是用于当作背景的数据传输，就调用父类的方法。"""
        super().send_message(data, True, path)