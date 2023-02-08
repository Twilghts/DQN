import collections
import copy
import time

_ip = ['10.0.0.' + str(n) for n in range(100)]


class Router:
    def __init__(self, number: int, speed=0.1, datasize=100):
        self.sign = number  # 路由器的序号
        self._ip = _ip[number]  # ip地址
        self.datasize = datasize  # 队列的最大数据接收量
        self.send_queue = collections.deque(maxlen=datasize)  # 发送队列
        self.send_occupation = 0  # 发送队列数据占用量
        self.receive_queue = collections.deque(maxlen=datasize)  # 接收队列
        self.receive_occupation = 0  # 接受队列数据占用量
        self.routing_table = collections.defaultdict()  # 路由表
        self.routing_table.default_factory = None
        self.speed = speed  # 单位为mb/ms
        self.receive_sign = (0, number)  # 接收队列标志
        self.send_sign = (number, 0)  # 发送队列标志
        self.handling_capacity = []  # 用于计算吞吐量的列表，内部元素应该是一个个元组，每一个元组代表着路由器吞吐量的变化

    def __str__(self):
        return f'Router:{self.sign}'

    def __repr__(self):
        return f'Router:{self.sign}'

    """获取发送队列的可用数据量"""
    def get_send_size(self):
        return self.datasize - self.send_occupation

    """获取接收队列的可用数据量"""
    def get_receive_size(self):
        return self.datasize - self.receive_occupation

    """将数据从接收队列发送到发送队列"""
    def from_receive_queue_send_queue(self, data):
        self.receive_occupation -= len(data)
        # self.send_queue.append(data)
        self.send_occupation += len(data)
        data.state = self.send_sign
        if data.state[0] == data.get_start():
            """信息第一次传递时的特殊对待"""
            data.log_delay = time.perf_counter()  # 为信息传递开启时间记录
            data.log.append(self.send_sign[0])  # 为信息记录增添起始路由器信息
        else:
            data.loging()  # 进行常规记录

    """从发送队列出队之后要修正发送队列的可用数据量"""
    def pop_send_queue(self, data):
        self.send_occupation -= len(data)

    """将数据发送至接受队列,传输失败返回False,传输成功返回True"""
    def put_receive_queue(self, data):
        if len(data) > self.get_receive_size():
            """如果数据包的大小大于路由器的接收队列，直接丢弃,并且进行记录"""
            data.log.append(self.receive_sign[1])
            data.log.append(-1)
            data.log.append(self.receive_sign[1])
            data.log.append(self.receive_sign[1] == data.get_goal())
            data.logs.append(copy.deepcopy(data.log))
            data.log.clear()
            return True
        elif self.receive_occupation >= self.datasize * 0.5 and len(data) >= 0.1 * self.datasize:
            """如果接收队列的余量小于最大存储量的50%并且数据包的大小大于最大存储量的10%，也进行丢弃。"""
            data.log.append(self.receive_sign[1])
            data.log.append(-1)
            data.log.append(self.receive_sign[1])
            data.log.append(self.receive_sign[1] == data.get_goal())
            data.logs.append(copy.deepcopy(data.log))
            data.log.clear()
            return True
        else:
            """否则入队"""
            # self.receive_queue.append(data)  # 添加数据
            self.receive_occupation += len(data)  # 修改数据量
            data.state = self.receive_sign  # 修改状态
            return False