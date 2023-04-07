from queue import Queue


class Link:
    def __init__(self, ports: tuple, length=10 ** 5, datasize=1000):
        self.link_deque = Queue(maxsize=datasize)  # 信道长度，设置最大传输数据量
        self.length: int = length  # 链路长度
        self.ports: tuple = ports  # 链路两端连接的路由器序号
        self.max_datasize: int = datasize  # 链路能承载的最大数据量
        self.throughput = 0

    def __str__(self):
        return f'Link({self.ports})。吞吐量为:{self.throughput}'

    def __repr__(self):
        return f'Link{self.ports}。吞吐量为:{self.throughput}'

    """将数据发送至链路的传输队列中"""

    def put_data(self, data):
        self.link_deque.put(data)
        self.throughput += 1

    """数据从传输队列出队后，更新链路传输对列数据可用量"""

    def pop_data(self):
        if not self.link_deque.empty():
            return self.link_deque.get()
        else:
            return None