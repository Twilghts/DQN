import threading
import time

import numpy as np

from rip_network import Rip

_interval_time = 0.01  # 数据包发送的间隔时间。

if __name__ == '__main__':
    start_time = time.perf_counter()
    rip_net = Rip()
    average_loss = []  # 计算平均丢包率。
    average_time = []  # 计算平均传播时延。
    """训练模型的全过程。"""
    for i in range(25):
        """每传输一次数据，就把路由器的吞吐量记录清零"""
        for router in rip_net.routers.values():
            router.handling_capacity.clear()
        rip_net.logs.clear()  # 每一轮发送信息之后清空记录。
        print(f'第{i + 1}次记录数据!')
        """准备进行网络拓扑中信息的传输!"""
        thread_pool = []  # 线程池
        rip_net.time = time.perf_counter()  # 更新网络开始时的时间戳，为计算吞吐量做准备
        print(len(rip_net.data_set))
        """正式启动信息发送"""
        for data in rip_net.data_set:
            task_thread = threading.Thread(target=rip_net.send_message,
                                           args=[data, False])  # 为每一个发送信息的过程创建线程
            # print(f'线程{task_thread.name}开启!')
            task_thread.start()  # 启动线程
            thread_pool.append(task_thread)  # 将线程添加到线程池
            time.sleep(_interval_time)  # 每隔_interval_time秒发送一个数据包
        """测试所有的线程是否存活，如果所有线程都结束运行，则主线程继续运行"""
        while True:
            for thread in thread_pool:
                """如果线程结束，从线程池中移除该线程，并打印出相关性息!"""
                if not thread.is_alive():
                    thread_pool.remove(thread)
            """如果线程池被清空，则继续运行!"""
            if len(thread_pool) == 0:
                break
        average_time.append(time.perf_counter() - rip_net.time)  # 计算传输过程中所消耗的总时间。
        """计算丢包率!"""
        gross = 0  # 数据包总量
        failure = 0  # 失败的数据包数量
        for logs in rip_net.logs.values():
            gross += 1
            if not logs[-1]:
                failure += 1
        print(f'丢包率:{round(failure / gross * 100, 3)}%')  # 保留三位小数
        average_loss.append(round(failure / gross * 100, 3))
        """更新数据包集合，并随机修改数据包大小."""
        rip_net.update_dataset(False)

    print(
        f'这次数据包的大小:{rip_net.data_size},数据包个数{rip_net.data_number}。Rip算法丢包率的集合:{average_loss}')
    print(
        f'这次数据包的大小:{rip_net.data_size},数据包个数{rip_net.data_number}。Rip算法的平均丢包率:{np.mean(average_loss)}%')
    # success = [item[1][-2] for item in rip_net.logs.items() if item[1][-1]]  # 传输成功的数据包的时延的列表。
    # failure = [item[1][-2] for item in rip_net.logs.items() if not item[1][-1]]  # 传输失败的数据包的时延的列表。
    # mixture = random.sample(success, 4)
    # mixture.extend(random.sample(failure, 1))
    # print(f'这次数据包的大小:{rip_net.data_size},数据包个数{rip_net.data_number}。'
    #       f'Rip算法的数据包的平均时延为:{np.around(numpy.mean(mixture), decimals=4)}')
    # for item in random.sample(list(rip_net.logs.items()), 1):
    #     print(f'数据包:{item[0]}的记录为{item[1]}')
    # for router in random.sample(list(rip_net.routers.values()), 1):
    print(f'一次数据传输过程中消耗的总时间平均为:{np.mean(average_time)}')
    print(f'路由器:{3}的吞吐量为:{rip_net.routers[3].handling_capacity}')
    print(f'消耗的总时间:{time.perf_counter() - start_time}秒')
