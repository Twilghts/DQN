import copy
import time

import networkx as nx

from net import Net


class Ospf(Net):
    def __init__(self):
        super().__init__()
        self.dynamic_graph = copy.deepcopy(self.G)  # 创建一个副本图，用于体现Ospf的动态性。

    """在传输信息的同时对网络进行动态更新"""
    def update_graph(self):
        """对每一个路由器进行访问，如果它的可用数据量小于一半，就对图中的边相应的权值进行修改，如果它的可用数据量正常，则将边的权值恢复成原图的权值"""
        modificate_edges: set = set()  # 统计所有被修改过的边。
        for router in self.routers.values():
            """可用数据量不够，进行修改。"""
            if router.get_receive_size() < router.datasize * 0.3:
                """获取直接与该节点相接的链路。"""
                edges: set = {(u, v) for u, v in self.dynamic_graph.edges if u == router.sign or v == router.sign}
                """修改每一条链路的权值。edge为元组"""
                for edge in edges:
                    self.dynamic_graph[edge[0]][edge[1]]['weight'] = 100
                modificate_edges |= edges  # 两个集合做并集。不会有重复元素。
        """获取所有未经修改的边。"""
        dismodificate_edges: set = {(u, v) for u, v in self.dynamic_graph.edges if (u, v) not in modificate_edges}
        """将未修改的边的权值恢复"""
        for u, v in dismodificate_edges:
            self.dynamic_graph[u][v]['weight'] = self.G[u][v]['weight']

    """每次结束一整次传输信息时，对图进行全局复原。"""
    def retry_graph(self):
        self.dynamic_graph = copy.deepcopy(self.G)

    def send_message(self, data, is_dqn=False, path=None):
        """动态的计算最佳路径"""
        state: int = data.get_start()  # 数据包最开始的状态
        action: int = nx.dijkstra_path(self.dynamic_graph, data.get_start(), data.get_goal())[1]  # 动态的计算数据包所要经过的下一跳路由器。
        start_time: float = time.perf_counter()
        """将信息放到第一个路由器的接收队列,如果路由器的可用数据量大于总数据量的一半时执行此操作。"""
        while True:
            if self.routers[data.get_start()].get_receive_size() >= self.router_datasize * 0.5:
                self.routers[data.get_start()].put_receive_queue(data)  # 信息进入等待队列
                self.calculate_handling_capacity(data.get_start(), self.router_power)  # 更新路由器的吞吐量(入第一个路由器)
                time.sleep(len(data) / self.router_power)  # 信息在路由器接收队列的处理时间
                break
            else:
                time.sleep(self.waiting_time)  # 轮询等待时间
        while True:
            """当信息不在发送队列时一直轮询"""
            while True:
                if len(data) <= self.routers[state].get_send_size():
                    self.routers[state].from_receive_queue_send_queue(data)  # 信息从接收队列移至发送队列,进行常规记录。
                    time.sleep(len(data) / self.router_power)  # 信息在路由器发送队列的处理时间
                    break
                else:
                    time.sleep(self.waiting_time)  # 轮询等待时间
            link_message: tuple = (state, action)  # 确定链路两个节点的前后顺序
            if (action, state) in self.links.keys():
                link_message: tuple = (action, state)
            """当信息不在链路上时一直轮询"""
            while True:
                if len(data) <= self.links[link_message].read_data_size():
                    self.routers[state].pop_send_queue(data)  # 信息从发送队列出队
                    self.calculate_handling_capacity(state, -self.router_power)  # 更新路由器的吞吐量(出路由器)
                    self.links[link_message].put_data(data, link_message)  # 信息进入链路中
                    time.sleep(self.links[link_message].delay)  # 信息在链路上的传递时间
                    break
                else:
                    time.sleep(self.waiting_time)  # 轮询等待时间
            """此时信息已从链路上传递完成"""
            self.links[link_message].pop_data(data)  # 信息从链路中出队，不再等待
            is_loss_package: bool = self.routers[action].put_receive_queue(data)  # 信息从下一个接收队列入队，有丢包风险
            if is_loss_package:
                """当数据包未能成功传输时所作的记录"""
                self.logs[data] = copy.deepcopy(data.logs)
                self.logs[data].append(round(time.perf_counter() - start_time, 5))  # 统计总共的消耗时间
                self.logs[data].append(False)
                break
            self.calculate_handling_capacity(action, self.router_power)  # 更新路由器的吞吐量(入下一个路由器)
            time.sleep(len(data) / self.router_power)  # 数据包在下一跳路由器等待队列中的处理时间
            """当数据包进入目标路由器时，与进入起始路由器时同样进行特殊处理，此时数据包成功传输到目标"""
            if data.state == (0, data.get_goal()):
                """信息从最后一个路由器的接收队列进入最后一个路由器的发送队列"""
                while True:
                    if len(data) <= self.routers[data.get_goal()].get_send_size():
                        self.routers[data.get_goal()].from_receive_queue_send_queue(data)  # 信息从接收队列移至发送队列,进行常规记录。
                        time.sleep(len(data) / self.router_power)  # 信息在路由器发送队列的处理时间
                        break
                    else:
                        time.sleep(self.waiting_time)  # 轮询等待时间
                self.routers[data.get_goal()].pop_send_queue(data)  # 信息从从最后一个路由器的发送队列出队
                self.calculate_handling_capacity(data.get_goal(), -self.router_power)  # 更新路由器的吞吐量(出最后一个路由器)
                """当数据包成功传输时所作的记录"""
                self.logs[data]: list = copy.deepcopy(data.logs)
                self.logs[data].append(round(time.perf_counter() - start_time, 5))  # 统计总共的消耗时间,保留五位小数。
                self.logs[data].append(True)
                break
            else:
                """动态更新数据包下一跳要到达的路由器。"""
                state: int = action
                action: int = nx.dijkstra_path(self.dynamic_graph, state, data.get_goal())[1]