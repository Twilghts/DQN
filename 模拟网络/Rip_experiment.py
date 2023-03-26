import time

from rip_network import Rip

if __name__ == '__main__':
    rip_network = Rip()
    start_time: float = time.perf_counter()
    for i in range(10):
        rip_network.update_dataset()
        for j in range(10):
            rip_network.update_dataset(is_create_data=False)
    while True:
        rip_network.update_dataset(is_create_data=False)
        state = [item[0] for item in rip_network.get_net_state().values()]
        if not any(state):  # 所有路由器全为空
            print(rip_network.get_net_state())
            break
    print(f'消耗时间:{time.perf_counter() - start_time}')
