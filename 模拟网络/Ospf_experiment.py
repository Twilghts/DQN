import threading
import time

import numpy as np

from ospf_network import Ospf

_interval_time = 0.01  # 数据包发送的间隔时间。
_update_interval_time = 0.02  # 动态更新全局网络间隔的时间

if __name__ == '__main__':
    start_time: float = time.perf_counter()
    ospf_net_ = Ospf()
    average_loss: list = []  # 计算平均丢包率。
    average_time: list = []  # 计算平均总时间。
    """训练模型的全过程。"""
    for i in range(25):
        """每传输一次数据，就把路由器的吞吐量记录清零"""
        for router in ospf_net_.routers.values():
            router.handling_capacity.clear()
        ospf_net_.logs.clear()  # 每一轮发送信息之后清空记录。
        print(f'第{i + 1}次记录数据!')
        """准备进行网络拓扑中信息的传输!"""
        thread_pool: list = []  # 线程池
        print(len(ospf_net_.data_set))
        ospf_net_.time = time.perf_counter()  # 更新网络开始时的时间戳，为计算吞吐量做准备
        count: int = 1  # 计算更新网络的次数，每0.2秒全局更新一次
        """正式启动信息发送"""
        for data in ospf_net_.data_set:
            task_thread = threading.Thread(target=ospf_net_.send_message,
                                           args=[data, False])  # 为每一个发送信息的过程创建线程
            # print(f'线程{task_thread.name}开启!')
            task_thread.start()  # 启动线程
            thread_pool.append(task_thread)  # 将线程添加到线程池
            time.sleep(_interval_time)  # 每隔_interval_time秒发送一个数据包
            if time.perf_counter() - ospf_net_.time >= count * _update_interval_time:
                ospf_net_.update_graph()
                count += 1
        """测试所有的线程是否存活，如果所有线程都结束运行，则主线程继续运行"""
        while True:
            for thread in thread_pool:
                """如果线程结束，从线程池中移除该线程，并打印出相关性息!"""
                if not thread.is_alive():
                    thread_pool.remove(thread)
                    # print(f'线程{thread.name}结束运行')
            """如果线程池被清空，则继续运行!"""
            if len(thread_pool) == 0:
                break
        average_time.append(time.perf_counter() - ospf_net_.time)  # 计算传输过程中所消耗的总时间。
        """计算丢包率!"""
        gross: int = 0  # 数据包总量
        failure: int = 0  # 失败的数据包数量
        for logs in ospf_net_.logs.values():
            gross += 1
            if not logs[-1]:
                failure += 1
        print(f'丢包率:{round(failure / gross * 100, 3)}%')  # 保留三位小数
        average_loss.append(round(failure / gross * 100, 3))
        """每一次发送信息之后训练数据。"""
        """更新数据包集合，并随机修改数据包大小."""
        ospf_net_.update_dataset(False)
        """将拷贝图回滚到初始状态。"""
        ospf_net_.retry_graph()

    print(
        f'这次数据包的大小:{ospf_net_.data_size},数据包个数{ospf_net_.data_number}。Ospf算法丢包率的集合:{average_loss}')
    print(
        f'这次数据包的大小:{ospf_net_.data_size},数据包个数{ospf_net_.data_number}。Ospf算法的平均丢包率:{np.mean(average_loss)}%')
    # success = [item[1][-2] for item in ospf_net_.logs.items() if item[1][-1]]  # 传输成功的数据包的时延的列表。
    # failure = [item[1][-2] for item in ospf_net_.logs.items() if not item[1][-1]]  # 传输失败的数据包的时延的列表。
    # mixture = random.sample(success, 4)
    # mixture.extend(random.sample(failure, 1))
    # print(f'这次数据包的大小:{ospf_net_.data_size},数据包个数{ospf_net_.data_number}。'
    #       f'Ospf算法的数据包的平均时延为:{np.around(numpy.mean(mixture), decimals=4)}')
    # for item in random.sample(list(ospf_net_.logs.items()), 1):
    #     print(f'数据包:{item[0]}的记录为{item[1]}')
    # for router in random.sample(list(ospf_net_.routers.values()), 1):
    #     print(f'路由器:{router}的吞吐量为:{router.handling_capacity}')
    print(f'一次完整的数据传输过程中消耗的时间为:{np.mean(average_time)}')
    print(f'路由器:{3}的吞吐量为:{ospf_net_.routers[3].handling_capacity}')
    print(f'消耗的总时间:{time.perf_counter() - start_time}秒')
