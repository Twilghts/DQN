import collections


class Link:
    def __init__(self, ports: tuple, length=10 ** 5, datasize=100, delay=0.5):
        self.link_deque = collections.deque(maxlen=datasize)  # 信道长度，设置最大传输数据量
        self.length: int = length  # 链路长度
        self.ports: tuple = ports  # 链路两端连接的路由器序号
        self.delay: float = delay  # 单位为秒
        self.occupation: int = 0  # 占用量
        self.max_datasize: int = datasize  # 链路能承载的最大数据量

    def __str__(self):
        return f'Link({self.ports}),长度为{self.delay}'

    def __repr__(self):
        return f'Link{self.ports},长度为{self.delay}'

    def transfer_time(self, data):
        if len(data) < (self.max_datasize - self.occupation):
            return self.delay * self.length

    """获取链路传输队列中的可用数据量"""
    def read_data_size(self):
        return self.max_datasize - self.occupation

    """将数据发送至链路的传输队列中"""
    def put_data(self, data, state):
        # self.link_deque.append(data)
        self.occupation += len(data)
        data.state = state

    """数据从传输队列出队后，更新链路传输对列数据可用量"""
    def pop_data(self, data):
        self.occupation -= len(data)
