import logging
import time

import numpy as np

from ospf_network import Ospf

if __name__ == '__main__':
    cache_size: int = 50
    logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    ospf_network = Ospf()
    start_time: float = time.perf_counter()
    loss_sets = []
    for episode in range(1):
        ospf_network.total_data_number = 0
        ospf_network.success_data_number = 0
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
        print(f'消耗时间:{time.perf_counter() - start_time}')
        print(
            f'丢包率:{(ospf_network.total_data_number - ospf_network.success_data_number) / ospf_network.total_data_number}')
        loss_sets.append(
            (ospf_network.total_data_number - ospf_network.success_data_number) / ospf_network.total_data_number)
    print(f'OSPF:{np.around(np.average(loss_sets), 6)}')
    logging.info(f'OSPF：每创建一次数据包后单纯发送的次数:{cache_size},丢包率:{np.around(np.average(loss_sets), 6)}\n'
                 f'数据包发送速率:{ospf_network.data_number},数据包的大小:{ospf_network.data_size}')