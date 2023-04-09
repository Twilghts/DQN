import logging
import time

import numpy as np
import tensorflow as tf

from dqn_network import DqnNetworkAgent

_batch_size: int = 256  # 每次训练的数据组的数量。
_is_best = True

if __name__ == '__main__':
    cache_size: int = 10
    create_size: int = 10
    logging.basicConfig(filename='log_for_dqn.log', encoding='utf-8', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    dqn_net_agent = DqnNetworkAgent()
    # average_loss: list = []  # 计算平均丢包率。
    # average_time: list = []  # 计算平均传播时延。
    model = tf.keras.models.load_model('model_5.h5')  # 加载模型
    dqn_net_agent.model = model
    start_time: float = time.perf_counter()
    # for step in range(30, 100, 10):
    delay_set = []  # 丢包率的集合
    delay_sets = []  # 单次传输的时延
    loss_sets = []  # 每次传输的时延的集合
    throughput_sets = []  # 每次传输的吞吐量总和
    throughput_capacity = 0  # 单次传输的吞吐量
    throughput_set = []
    for episode in range(10):
        """每次传输后路由器吞吐量归零"""
        for router in dqn_net_agent.routers.values():
            router.total = 0
            router.failure = 0
        """每次传输后链路吞吐量归零"""
        for link in dqn_net_agent.links.values():
            link.throughput = 0
        throughput_capacity = 0
        throughput_set.clear()
        delay_set.clear()
        dqn_net_agent.memory.clear()
        dqn_net_agent.total_data_number = 0
        dqn_net_agent.success_data_number = 0
        dqn_net_agent.packet_for_record.clear()
        for i in range(create_size):
            dqn_net_agent.update_dataset(is_best=_is_best)
            throughput_set.append(min(dqn_net_agent.get_net_state().values()))
            for j in range(cache_size):
                dqn_net_agent.update_dataset(is_create_data=False, is_best=_is_best)
                # throughput_set.append(min(dqn_net_agent.get_net_state().values()))
        while True:
            dqn_net_agent.update_dataset(is_create_data=False, is_best=_is_best)
            state = [item for item in dqn_net_agent.get_net_state().values()]
            if not any(state):  # 所有路由器全为空
                print(f'第{episode + 1}轮训练**************************************')
                # print(dqn_net_agent.get_net_state())
                break
        for data in dqn_net_agent.packet_for_record:
            for record in data.logs:
                if record[-3] != -100:
                    delay_set.append(record[-3])
                # else:
                #     delay_set.append(-5)
        print(f'本次传输的数据包总量:{dqn_net_agent.total_data_number}')
        # """统计单次传输中的吞吐量"""
        # for router in dqn_net_agent.routers.values():
        #     throughput_capacity += router.total - router.failure
        loss_sets.append(
            (dqn_net_agent.total_data_number - dqn_net_agent.success_data_number) / dqn_net_agent.total_data_number)
        # throughput_capacity += np.average([link.throughput for link in dqn_net_agent.links.values()]) * (
        #             1 - loss_sets[-1])
        # throughput_sets.append(throughput_capacity)  # 计算单次传输中的吞吐量
        throughput_sets.append(np.average(throughput_set))  # 计算单次传输中的吞吐量
        # for data in dqn_net_agent.packet_for_record:
        #     if not data.logs[-1][-1]:
        #         print(data.shortest_path, data.logs)
        # for data in dqn_net_agent.packet_for_train:
        #     for log in data.logs:
        #         dqn_net_agent.remember(*log)
        #     print(data.shortest_path, data.logs)
        # dqn_net_agent.replay(_batch_size, dqn_net_agent.G)
        print(
            f'丢包率:{(dqn_net_agent.total_data_number - dqn_net_agent.success_data_number) / dqn_net_agent.total_data_number}')
        delay_sets.append(-(sum(delay_set) * (1 + loss_sets[-1] * 3) / dqn_net_agent.total_data_number))  # 统计单次模拟的时延
        print(f'时延:{delay_sets[-1]}')
        print(f'吞吐量:{throughput_sets[-1]}\n')
        # logging.info(
        #     f'DQN：每创建一次数据包后单纯发送的次数:{cache_size},丢包率:{np.around(loss_sets[-1], 6)}\n'
        #     f'数据包发送总数:{dqn_net_agent.total_data_number},数据包的大小:{dqn_net_agent.data_size}')
    # dqn_net_agent.model.save('model_5.h5')
    print(f'DQN平均丢包率:{np.around(np.average(loss_sets), 4)},平均时延:{np.average(delay_sets)},'
          f'平均吞吐量:{np.average(throughput_sets)}')
    # logging.info(f'RIP：每创建一次数据包后单纯发送的次数:{cache_size},丢包率:{np.around(np.average(loss_sets), 6)}\n'
    #              f'数据包发送速率:{dqn_net_agent.data_number},数据包的大小:{dqn_net_agent.data_size}')
    print(f'消耗时间:{time.perf_counter() - start_time}')
    logging.info(
        f'DQN：每创建一次数据包后单纯发送的次数:{cache_size},丢包率:{np.around(np.average(loss_sets), 4)}\n'
        f'数据包发送速率:{dqn_net_agent.data_number}Gbps,数据包的大小:{dqn_net_agent.data_size}Kb,'
        f'平均时延:{np.average(delay_sets)}ms,平均吞吐量:{np.average(throughput_sets)}Gbps')
# """训练模型的全过程。"""
# for i in range(1000):
#     print(f'第{i + 1}次记录并训练数据!')
#     """准备进行网络拓扑中信息的传输!"""
#     thread_pool: list = []  # 线程池
#     for data in dqn_net_agent.data_set:
#         P: set = dqn_net_agent.k_shortest_paths_by_dqn(data)
#         path: tuple = dqn_net_agent.choose_path(P)
#         data.shortest_path = path
#     dqn_net_agent.time = time.perf_counter()  # 更新网络开始时的时间戳，为计算吞吐量做准备
#     print(len(dqn_net_agent.data_set))
#     """正式启动信息发送"""
#     for data in dqn_net_agent.data_set:
#         task_thread = threading.Thread(target=dqn_net_agent.send_message,
#                                        args=[data, True, data.shortest_path])  # 为每一个发送信息的过程创建线程
#         # print(f'线程{task_thread.name}开启!')
#         task_thread.start()  # 启动线程
#         thread_pool.append(task_thread)  # 将线程添加到线程池
#         time.sleep(_interval_time)  # 每隔_interval_time秒发送一个数据包
#     """测试所有的线程是否存活，如果所有线程都结束运行，则主线程继续运行"""
#     while True:
#         for thread in thread_pool:
#             """如果线程结束，从线程池中移除该线程，并打印出相关性息!"""
#             if not thread.is_alive():
#                 thread_pool.remove(thread)
#                 # print(f'线程{thread.name}结束运行')
#         """如果线程池被清空，则继续运行!"""
#         if len(thread_pool) == 0:
#             break
#     average_time.append(time.perf_counter() - dqn_net_agent.time)  # 计算传输过程中所消耗的总时间。
#     """计算丢包率!"""
#     gross: int = 0  # 数据包总量
#     failure: int = 0  # 失败的数据包数量
#     for logs in dqn_net_agent.logs.values():
#         for log_for_dqn.log in logs[:-2]:
#             if len(log_for_dqn.log) == 5:
#                 dqn_net_agent.remember(*log_for_dqn.log)
#         gross += 1
#         if not logs[-1]:
#             failure += 1
#     print(f'丢包率:{round(failure / gross * 100, 3)}%')  # 保留三位小数
#     average_loss.append(round(failure / gross * 100, 3))
#     dqn_net_agent.logs.clear()  # 每一轮发送信息之后清空记录。
#     """每传输一次数据，就把路由器的吞吐量记录清零"""
#     for router in dqn_net_agent.routers.values():
#         router.handling_capacity.clear()
#     """每一次发送信息之后训练数据。"""
#     if len(dqn_net_agent.memory) >= _batch_size:
#         dqn_net_agent.replay(_batch_size, dqn_net_agent.G)
#     """更新数据包集合，并随机修改数据包大小."""
#     dqn_net_agent.update_dataset(False)
#
# print(
#     f'这次数据包的起止大小:{(dqn_net_agent.size_min, dqn_net_agent.size_max)}。训练过程中的丢包率的集合:{average_loss}')
# print(
#     f'这次数据包的起止大小:{(dqn_net_agent.size_min, dqn_net_agent.size_max)}。训练过程中的平均丢包率:{np.mean(average_loss)}%')
# average_loss.clear()  # 接下来求使用DQN算法求出来的平均丢包率。
# dqn_net_agent.model.save('model_7.h5')
