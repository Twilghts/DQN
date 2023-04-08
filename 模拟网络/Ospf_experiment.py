import logging
import time

import numpy as np

from ospf_network import Ospf

if __name__ == '__main__':
    cache_size: int = 10
    logging.basicConfig(filename='log_for_ospf.log', encoding='utf-8', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    ospf_network = Ospf()
    start_time: float = time.perf_counter()
    loss_sets = []  # 丢包率的集合
    delay_set = []  # 单次传输的时延
    delay_sets = []  # 每次传输的时延的集合
    throughput_set = []  # 每次传输的吞吐量总和
    throughput_capacity = 0  # 单次传输的吞吐量
    for episode in range(25):
        """每次传输后路由器吞吐量归零"""
        for router in ospf_network.routers.values():
            router.total = 0
            router.failure = 0
        """每次传输后链路吞吐量归零"""
        for link in ospf_network.links.values():
            link.throughput = 0
        throughput_capacity = 0
        delay_set.clear()
        ospf_network.total_data_number = 0
        ospf_network.success_data_number = 0
        ospf_network.packet_for_record.clear()
        for i in range(10):
            ospf_network.update_dataset()
            for j in range(cache_size):
                ospf_network.update_dataset(is_create_data=False)
        while True:
            ospf_network.update_dataset(is_create_data=False)
            state = [item[0] for item in ospf_network.get_net_state().values()]
            if not any(state):  # 所有路由器全为空
                ospf_network.retry_graph()
                break
        # for data in ospf_network.data_set:
        #     if len(data.logs) != 0 and not data.logs[-1][-1]:
        #         print(data.shortest_path, data.logs)
        loss_sets.append(
            (ospf_network.total_data_number - ospf_network.success_data_number) / ospf_network.total_data_number)
        for data in ospf_network.packet_for_record:
            for record in data.logs:
                if record[-3] != -100:
                    delay_set.append(record[-3])
                # else:
                #     delay_set.append(-5)
        print(f'本次传输的数据包总量:{ospf_network.total_data_number}')
        # """以路由器为基础计算吞吐量"""
        # for router in ospf_network.routers.values():
        #     throughput_capacity += router.total - router.failure
        throughput_capacity += np.average([link.throughput for link in ospf_network.links.values()]) * (
                1 - loss_sets[-1])
        throughput_set.append(throughput_capacity)  # 计算单次传输中的吞吐量
        print(f'消耗时间:{time.perf_counter() - start_time}')
        print(
            f'丢包率:{(ospf_network.total_data_number - ospf_network.success_data_number) / ospf_network.total_data_number}')
        delay_sets.append(-(sum(delay_set) * (1 + loss_sets[-1] * 3) / ospf_network.total_data_number))  # 统计单次模拟的时延
        print(f'时延:{delay_sets[-1]}')
        print(f'吞吐量:{throughput_set[-1]}\n')
    print(f'OSPF的平均丢包率:{np.around(np.average(loss_sets), 6)},平均时延:{np.average(delay_sets)},'
          f'平均吞吐量:{np.average(throughput_set)}')
    logging.info(f'OSPF：每创建一次数据包后单纯发送的次数:{cache_size},丢包率:{np.around(np.average(loss_sets), 6)}\n'
                 f'数据包发送速率:{ospf_network.data_number},数据包的大小:{ospf_network.data_size}'
                 f'平均时延:{np.average(delay_sets)},平均吞吐量:{np.average(throughput_set)}')
