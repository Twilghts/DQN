import copy
import time


class Data:
    def __init__(self, start, target, is_privacy, size=600, delay=0):
        self.is_privacy = is_privacy
        self._start = start  # 起始路由器标号
        self._target = target  # 终止路由器标号
        self._size = size  # 数据包大小
        self.delay = delay  # 计算数据包传送中经过的时间
        self.state: tuple = (0, start)  # 数据包的状态
        self.shortest_path = []  # 从起点到终点的最短路径
        self.log_delay = 0
        self.logs = []  # 传递过程中记录的集合
        self.log = []  # 信息传递过程中的每条记录
        self.flag = 0  # flag标志位，标志数据是否隐私,0代表隐私数据，1代表公开数据

    def __repr__(self):
        return f'Data({self._start},{self._target}),数据量为{self._size}'

    def __str__(self):
        return f'Data({self._start},{self._target}),数据量为{self._size}'

    def __len__(self):
        return self._size

    def get_state(self):
        return self.state

    def get_size(self):
        return self._size

    def get_goal(self):
        return self._target

    def get_start(self):
        return self._start

    def get_mark(self):
        return self._start, self._target

    """记录数据，是DQN训练的重要保障"""
    def loging(self):
        self.log.append(self.state[0])  # 为记录增添目标路由器(action)
        self.log.append(-round(time.perf_counter() - self.log_delay, 4))  # 为记录增添时间记录(reword),保留五位小数。
        self.log.append(self.state[0])  # 为记录增添目标路由器(next_state)
        self.log.append(self.state[0] == self._target)
        # if len(self.log) != 5:
        #     time.sleep(10)
        self.logs.append(copy.deepcopy(self.log))  # 为记录集合增添记录
        self.log.clear()  # 记录清零
        self.log_delay = time.perf_counter()  # 下一次记录(action)的起始时间
        self.log.append(self.state[0])  # 下一次记录的state
