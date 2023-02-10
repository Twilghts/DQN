from net import Net
from 模拟网络.DQN import DQN
from 模拟网络.利用network实现k最短路径算法 import k_shortest_paths


class DqnNetworkAgent(Net, DQN):
    def __init__(self):
        Net.__init__(self)
        DQN.__init__(self, state_size=1, action_size=len(self.G.nodes))
        self._k = 4  # k最短路径算法中路径的条数

    def k_shortest_paths_by_dqn(self, data):
        return k_shortest_paths(self.G, data.get_start(), data.get_goal(), self._k)

    def send_message(self, data, is_dqn=True, path=None):
        """如果是用于当作背景的数据传输，就调用父类的方法。"""
        super().send_message(data, True, path)
        # path = []
        # _start_time = time.perf_counter()
        # count = 0  # 传输信息的次数,如果传三十次都传不好，就快速失败。
        # """将信息放到第一个路由器的接收队列"""
        # while True:
        #     if len(data) <= self.routers[data.get_start()].get_receive_size():
        #         self.routers[data.get_start()].put_receive_queue(data)  # 信息进入等待队列
        #         self.calculate_handling_capacity(data.get_start(), self.router_power)  # 更新路由器的吞吐量(入第一个路由器)
        #         time.sleep(len(data) / self.router_power)  # 信息在路由器接收队列的处理时间
        #         break
        #     else:
        #         time.sleep(self.waiting_time)  # 轮询等待时间
        # path.append(data.get_start())
        # state = data.get_start()  # 起始状态（起始路由器）
        # action = self.choose_path(data.get_start())  # 第一个动作
        # while True:
        #     """当信息不在发送队列时一直轮询"""
        #     while True:
        #         if len(data) <= self.routers[state].get_send_size():
        #             self.routers[state].from_receive_queue_send_queue(data)  # 信息从接收队列移至发送队列,进行常规记录。
        #             time.sleep(len(data) / self.router_power)  # 信息在路由器发送队列的处理时间
        #             break
        #         else:
        #             time.sleep(self.waiting_time)  # 轮询等待时间
        #     link_message = (state, action)  # 确定链路两个节点的前后顺序
        #     if (action, state) in self.links.keys():
        #         link_message = (action, state)
        #     """当信息不在链路上时一直轮询"""
        #     while True:
        #         if len(data) <= self.links[link_message].read_data_size():
        #             self.routers[state].pop_send_queue(data)  # 信息从发送队列出队
        #             self.calculate_handling_capacity(state, -self.router_power)  # 更新路由器的吞吐量(出路由器)
        #             self.links[link_message].put_data(data, link_message)  # 信息进入链路中
        #             time.sleep(self.links[link_message].delay)  # 信息在链路上的传递时间
        #             break
        #         else:
        #             time.sleep(self.waiting_time)  # 轮询等待时间
        #     """此时信息已从链路上传递完成"""
        #     self.links[link_message].pop_data(data)  # 信息从链路中出队，不再等待
        #     is_loss_package = self.routers[action].put_receive_queue(data)  # 信息从下一个接收队列入队，有丢包风险
        #     if is_loss_package or count >= 15:
        #         """当数据包未能成功传输或者传输次数过大时时所作的记录"""
        #         """如果信息传输成功而传输次数过大时，进行特殊处理"""
        #         if count >= 15 and not is_loss_package:
        #             self.routers[action].from_receive_queue_send_queue(data)
        #             self.routers[action].pop_send_queue(data)  # 信息从从最后一个路由器的发送队列出队
        #         """如果是用于dqn训练的数据，则进行记录，否则，不会进行记录。"""
        #         self.logs[data] = copy.deepcopy(data.logs)
        #         self.logs[data].append(round(time.perf_counter() - _start_time, 5))  # 统计总共的消耗时间
        #         self.logs[data].append(False)
        #         # print(f'一个数据包的传输记录{data.logs}')
        #         break
        #     time.sleep(len(data) / self.router_power)  # 数据包在下一跳路由器等待队列中的处理时间
        #     self.calculate_handling_capacity(action, self.router_power)  # 更新路由器的吞吐量(入下一个路由器)
        #     """当数据包进入目标路由器时，与进入起始路由器时同样进行特殊处理，此时数据包成功传输到目标"""
        #     if data.state == (0, data.get_goal()):
        #         """信息从最后一个路由器的接收队列进入最后一个路由器的发送队列"""
        #         self.routers[data.get_goal()].from_receive_queue_send_queue(data)
        #         self.routers[data.get_goal()].pop_send_queue(data)  # 信息从从最后一个路由器的发送队列出队
        #         self.calculate_handling_capacity(data.get_goal(), -self.router_power)  # 更新路由器的吞吐量(出最后一个路由器)
        #         """当数据包成功传输时所作的记录"""
        #         self.logs[data] = copy.deepcopy(data.logs)
        #         self.logs[data].append(round(time.perf_counter() - _start_time, 5))  # 统计总共的消耗时间,保留五位小数。
        #         self.logs[data].append(True)
        #         # print(f'一个数据包的传输记录{data.logs}')
        #         break
        #     else:
        #         state = action
        #         action = self.choose_path(state)
        #         count += 1
