import copy
import time


class Data:
    def __init__(self, start, target, size=600, delay=0):
        self._start: int = start  # 起始路由器标号
        self._target: int = target  # 终止路由器标号
        self.size: int = size  # 数据包大小
        self.delay: float = delay  # 计算数据包传送中经过的时间
        self.state: int = start  # 数据包的状态
        self.shortest_path: list = []  # 从起点到终点的最短路径
        self.log_delay: float = 0
        self.logs: list = []  # 传递过程中记录的集合
        self.flag: int = 0  # flag标志位，标志数据是否隐私,0代表隐私数据，1代表公开数据
        self.count = 0  # 数据包所经过的路由器的跳数

    def __repr__(self):
        return f'Data({self._start},{self._target}),数据量为{self.size}'

    def __str__(self):
        return f'Data({self._start},{self._target}),数据量为{self.size}'

    def __len__(self):
        return self.size

    def get_state(self):
        return self.state

    def get_size(self):
        return self.size

    def get_goal(self):
        return self._target

    def get_start(self):
        return self._start

    def get_mark(self):
        return self._start, self._target

    """记录数据，是DQN训练的重要保障"""

    def loging(self, number, old_state, new_state, is_loss=False, is_done=False):
        if is_loss:
            self.logs.append((old_state, new_state, -1000, new_state, is_done))
        else:
            self.logs.append((old_state, new_state, - (0.05 + (number + 1) * 0.01), new_state, is_done))