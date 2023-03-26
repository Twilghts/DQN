import time

import numpy as np

from rip_network import Rip

if __name__ == '__main__':
    rip_network = Rip()
    start_time: float = time.perf_counter()
    loss_sets = []
    for episode in range(100):
        for i in range(10):
            rip_network.update_dataset()
            for j in range(100):
                rip_network.update_dataset(is_create_data=False)
        while True:
            rip_network.update_dataset(is_create_data=False)
            state = [item[0] for item in rip_network.get_net_state().values()]
            if not any(state):  # 所有路由器全为空
                break
        print(f'消耗时间:{time.perf_counter() - start_time}')
        loss_set = [state[1] for state in rip_network.get_net_state().values()]
        print(np.average(loss_set))
        loss_sets.append(np.average(loss_set))
    print(f'RIP:{np.average(loss_sets)}')