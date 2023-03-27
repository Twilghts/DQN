import collections
from queue import Queue

_ip = ['10.0.0.' + str(n) for n in range(100)]
_datasize_min = 256
_datasize_max = 512
_weight_min = 1
_weight_max = 5
"""计算(处理速度--数据量大小)表达式"""


def compute_expression(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    expression = "({} * x) + {}".format(m, b)
    return expression


"""根据处理速度计算数据量大小"""


def calculate_ordinate(expression, x):
    return eval(expression.replace("x", str(x)))


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
        self.calculate_datasize()  # 根据路由器处理速度计算路由器数据量
        self.total = 0
        self.failure = 0

    def __str__(self):
        return f'Router:{self.sign}'

    def __repr__(self):
        return f'Router:{self.sign}'

    """路由器可接收的数据量大小受传输速度影响"""

    def calculate_datasize(self):
        expression = compute_expression(_weight_min, _datasize_min, _weight_max, _datasize_max)
        return calculate_ordinate(expression, self.speed)

    """从发送队列出队之后要修正发送队列的可用数据量"""

    def pop_send_queue(self):
        if not self.receive_queue.empty():
            data = self.receive_queue.get()
            self.cache -= len(data)
        else:
            data = None
        return data

    """将数据发送至接受队列,传输失败返回False,传输成功返回True"""

    def put_receive_queue(self, data):
        if len(data) + self.cache > self.datasize:
            self.failure += 1
            self.total += 1
            return False
        elif self.sign == data.get_goal():  # 成功传输至终点路由器
            self.total += 1
            return True
        else:
            self.receive_queue.put(data)
            self.total += 1
            self.cache += len(data)
            data.loging(self.cache // len(data))
            return False