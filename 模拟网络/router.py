import collections
from queue import Queue


class Router:
    def __init__(self, number: int, speed=10, datasize=256):
        self.sign: int = number  # 路由器的序号
        self.speed: float = speed  # 单位为mb/ms
        self.datasize: int = datasize
        self.receive_queue = Queue(maxsize=10000)  # 队列
        self.cache: int = 0  # 队列缓存
        self.routing_table: dict = collections.defaultdict()  # 路由表
        self.routing_table.default_factory = None
        self.handling_capacity: list = []  # 用于计算吞吐量的列表，内部元素应该是一个个元组，每一个元组代表着路由器吞吐量的变化
        self.total = 0
        self.failure = 0

    def __str__(self):
        return f'Router:{self.sign}'

    def __repr__(self):
        return f'Router:{self.sign}'
    """从发送队列出队之后要修正发送队列的可用数据量"""

    def pop_send_queue(self):
        if not self.receive_queue.empty():
            data = self.receive_queue.get()
            self.cache -= len(data)
        else:
            data = None
        return data

    """将数据发送至接受队列,传输失败返回False,传输成功返回True"""

    def put_receive_queue(self, data, old_state=-1, is_rip=False):
        if len(data) + self.cache > self.datasize:  # 数据包丢失
            self.failure += 1
            self.total += 1
            if old_state != -1:  # 第一跳路由器不做记录
                data.loging(self.cache // len(data), old_state=old_state, new_state=self.sign, is_loss=True,
                            is_rip=is_rip)
            return False, True  # 第一个逻辑值表示数据包是否已经成功传输到终点路由器，第二个逻辑值表示该数据包是否已经结束其生命周期
        elif self.sign == data.get_goal():  # 成功传输至终点路由器
            self.total += 1
            if old_state != -1:  # 第一跳路由器不做记录
                data.loging(self.cache // len(data), old_state=old_state, new_state=self.sign, is_done=True,
                            is_rip=is_rip)
            return True, True  # 第一个逻辑值表示数据包是否已经成功传输到终点路由器，第二个逻辑值表示该数据包是否已经结束其生命周期
        else:  # 还在传输过程中
            self.receive_queue.put(data)
            self.total += 1
            self.cache += len(data)
            if old_state != -1:  # 第一跳路由器不做记录
                data.loging(self.cache // len(data), old_state=old_state, new_state=self.sign, is_rip=is_rip)
            return False, False  # 第一个逻辑值表示数据包是否已经成功传输到终点路由器，第二个逻辑值表示该数据包是否已经结束其生命周期
