import copy
import random
import time

import matplotlib.pyplot as plt
import networkx as nx
import numpy

from data import Data
from link import Link
from router import Router


class Net:
    def __init__(self):
        self.data_number = 40
        self.G = nx.Graph()
        self.G.add_weighted_edges_from([(0, 1, 3.5), (0, 2, 3.0), (1, 2, 2.0), (1, 3, 2.5),
                                        (2, 5, 2.0), (3, 4, 7.0), (4, 5, 2.5), (5, 7, 1.5),
                                        (4, 8, 3.0), (7, 8, 2.0), (6, 7, 0.5), (6, 10, 2.0),
                                        (8, 9, 1.5), (9, 10, 0.5)])
        """路由器组 为字典，键为路由器的编号，值为所对应的路由器"""
        self.routers = {
            number: Router(number) for number in self.G.nodes
        }
        """构建每一个路由器的路由表"""
        for _router in self.routers.values():
            _router.routing_table = {
                node: nx.dijkstra_path(self.G, _router.sign, node) for node in self.G.nodes
            }
        """网络连接组 为字典，键为起始路由器和终止路由器的元组，值为相对应的网络链接。"""
        self.links = {
            (start, target): Link((start, target), delay=weight['weight'] / 100) for start, target, weight in
            self.G.edges(data=True)
        }
        """数据包集合，一共有指定数目个数据包,每个数据包的大小都不同。"""
        self.size_min = 600  # 数据包大小的最小值
        self.size_max = 700  # 数据包大小的最大值
        self.data_size = 700  # 数据包的大小
        """本数据集合用于充当背景环境。"""
        self.data_set = {Data(x, y, size=self.data_size, is_privacy=False) for x, y in
                         zip(numpy.random.choice(self.G.nodes, self.data_number),
                             numpy.random.choice(self.G.nodes, self.data_number)) if x != y}
        """信息流的记录信息,键为数据包本体，值为数据包在网络中传输的记录"""
        self.logs = {
            data: [] for data in self.data_set
        }
        self.time = 0  # 网络开始传输信息时的时间戳，用于计算吞吐量
        self.router_power = 30000  # 路由器信息处理能力
        self.waiting_time = 0.05  # 询问等待时间

    def update_dataset(self, is_privacy):
        """更新数据包内容。一部分是用于dqn训练，另一部分当作背景环境。
        :param is_privacy:
        """
        self.data_set = {Data(x, y, size=self.data_size, is_privacy=is_privacy) for x, y
                         in
                         zip(numpy.random.choice(self.G.nodes, self.data_number),
                             numpy.random.choice(self.G.nodes, self.data_number)) if x != y}

    def show_graph(self):
        # 使用spring布局绘制图形
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True)

        # 添加显示权重的边标签
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)

        # 显示绘图
        plt.show()

    def calculate_handling_capacity(self, router_sign, handling_capacity):
        if len(self.routers[router_sign].handling_capacity) == 0:
            self.routers[router_sign].handling_capacity.append((time.perf_counter() - self.time, handling_capacity))
        else:
            """基础数值等于路由器最后状态([-1])的吞吐量([1])"""
            base_value = self.routers[router_sign].handling_capacity[-1][1]
            new_value = base_value + handling_capacity
            self.routers[router_sign].handling_capacity.append((time.perf_counter() - self.time, new_value))

    def send_message(self, data, is_dqn, path=None):
        """获取从数据包出发点到达结束点的最短路径"""
        if is_dqn:
            data.shortest_path = path  # 如果该方法是DQN寻路时使用，则手动传递最短路径
        else:
            """否则则由传统算法计算最佳路径。"""
            data.shortest_path = self.routers[data.get_start()].routing_table[data.get_goal()]
        start_time = time.perf_counter()
        """将信息放到第一个路由器的接收队列"""
        while True:
            if len(data) <= self.routers[data.get_start()].get_receive_size():
                self.routers[data.get_start()].put_receive_queue(data)  # 信息进入等待队列
                self.calculate_handling_capacity(data.get_start(), self.router_power)  # 更新路由器的吞吐量(入第一个路由器)
                time.sleep(len(data) / self.router_power)  # 信息在路由器接收队列的处理时间
                break
            else:
                time.sleep(self.waiting_time)  # 轮询等待时间
        """每次循环从信息到达路由器的接收队列结束，直到目标路由器结束"""
        for sign in range(len(data.shortest_path) - 1):
            """当信息不在发送队列时一直轮询"""
            while True:
                if len(data) <= self.routers[data.shortest_path[sign]].get_send_size():
                    self.routers[data.shortest_path[sign]].from_receive_queue_send_queue(data)  # 信息从接收队列移至发送队列,进行常规记录。
                    time.sleep(len(data) / self.router_power)  # 信息在路由器发送队列的处理时间
                    break
                else:
                    time.sleep(self.waiting_time)  # 轮询等待时间
            link_message = (data.shortest_path[sign + 1], data.shortest_path[sign])  # 确定链路两个节点的前后顺序
            if (data.shortest_path[sign], data.shortest_path[sign + 1]) in self.links.keys():
                link_message = (data.shortest_path[sign], data.shortest_path[sign + 1])
            """当信息不在链路上时一直轮询"""
            while True:
                if len(data) <= self.links[link_message].read_data_size():
                    self.routers[data.shortest_path[sign]].pop_send_queue(data)  # 信息从发送队列出队
                    self.calculate_handling_capacity(data.shortest_path[sign], -self.router_power)  # 更新路由器的吞吐量(出路由器)
                    self.links[link_message].put_data(data, link_message)  # 信息进入链路中
                    time.sleep(self.links[link_message].delay)  # 信息在链路上的传递时间
                    break
                else:
                    time.sleep(self.waiting_time)  # 轮询等待时间
            """此时信息已从链路上传递完成"""
            self.links[link_message].pop_data(data)  # 信息从链路中出队，不再等待
            is_loss_package = self.routers[data.shortest_path[sign + 1]].put_receive_queue(data)  # 信息从下一个接收队列入队，有丢包风险
            if is_loss_package:
                """当数据包未能成功传输时所作的记录"""
                self.logs[data] = copy.deepcopy(data.logs)
                self.logs[data].append(time.perf_counter() - start_time)  # 统计总共的消耗时间
                self.logs[data].append(False)
                break
            time.sleep(len(data) / self.router_power)  # 数据包在下一跳路由器等待队列中的处理时间
            self.calculate_handling_capacity(data.shortest_path[sign + 1], self.router_power)  # 更新路由器的吞吐量(入下一个路由器)
        """当数据包进入目标路由器时，与进入起始路由器时同样进行特殊处理"""
        if data.state == (0, data.get_goal()):
            """信息从最后一个路由器的接收队列进入最后一个路由器的发送队列"""
            self.routers[data.get_goal()].from_receive_queue_send_queue(data)
            self.routers[data.get_goal()].pop_send_queue(data)  # 信息从从最后一个路由器的发送队列出队
            self.calculate_handling_capacity(data.get_goal(), -self.router_power)  # 更新路由器的吞吐量(出最后一个路由器)
            """当数据包成功传输时所作的记录"""
            self.logs[data] = copy.deepcopy(data.logs)
            self.logs[data].append(round(time.perf_counter() - start_time, 5))  # 统计总共的消耗时间,保留五位小数。
            self.logs[data].append(True)
