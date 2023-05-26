import collections
from enum import Enum
from queue import Queue


class TypeOfNode(Enum):
    computational_node = 1
    communication_node = 2
    sensor_node = 3


class Router:
    def __init__(self, number: int, speed=10, datasize=256):
        self.datasize = datasize
        self.sign: int = number  # 路由器的序号
        self.receive_queue = Queue(maxsize=10000)  # 队列
        self.cache: int = 0  # 队列缓存
        self.routing_table: dict = collections.defaultdict()  # 路由表
        self.routing_table.default_factory = None
        self.total = 0
        self.failure = 0
        self.computing_power = 200  # 算力单位MIPS/核
        self.number_of_kernel = 50  # 内核数量
        self.type = TypeOfNode.computational_node
        self.throughput = 100  # 吞吐量

    def __str__(self):
        return f'Router:{self.sign}'

    def __repr__(self):
        return f'Router:{self.sign}'

    """从发送队列出队之后要修正发送队列的可用数据量"""

    def pop_send_queue(self):
        data_set = set()
        data_size = 0
        while data_size < self.throughput:
            if self.receive_queue.empty():
                break
            else:
                data = self.receive_queue.get()
                self.cache -= len(data)
                data_size += len(data)
                data_set.add(data)
        return data_set

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
