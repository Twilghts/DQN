import threading
import time

import numpy as np

from ospf_network import Ospf

_interval_time = 0.05  # 数据包发送的间隔时间。

if __name__ == '__main__':
    ospf_net_ = Ospf()
    average_loss = []  # 计算平均丢包率。
    # model = tf.keras.models.load_model('model_1.h5')  # 加载模型
    # ospf_net_.model = model
    """训练模型的全过程。"""
    for i in range(25):
        print(f'第{i + 1}次记录数据!')
        """准备进行网络拓扑中信息的传输!"""
        thread_pool = []  # 线程池
        ospf_net_.time = time.perf_counter()  # 更新网络开始时的时间戳，为计算吞吐量做准备
        print(len(ospf_net_.data_set))
        """正式启动信息发送"""
        for data in ospf_net_.data_set:
            task_thread = threading.Thread(target=ospf_net_.send_message,
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
                    # print(f'线程{thread.name}结束运行')
            """如果线程池被清空，则继续运行!"""
            if len(thread_pool) == 0:
                break
        """计算丢包率!"""
        gross = 0  # 数据包总量
        failure = 0  # 失败的数据包数量
        for logs in ospf_net_.logs.values():
            gross += 1
            if not logs[-1]:
                failure += 1
        print(f'丢包率:{round(failure / gross * 100, 3)}%')  # 保留三位小数
        average_loss.append(round(failure / gross * 100, 3))
        ospf_net_.logs.clear()  # 每一轮发送信息之后清空记录。
        """每一次发送信息之后训练数据。"""
        """更新数据包集合，并随机修改数据包大小."""
        ospf_net_.update_dataset(False)

    print(
        f'这次数据包的大小:{ospf_net_.data_size}。传统算法丢包率的集合:{average_loss}')
    print(
        f'这次数据包的大小:{ospf_net_.data_size}。使用传统算法的平均丢包率:{np.mean(average_loss)}%')
    average_loss.clear()  # 接下来求使用DQN算法求出来的平均丢包率。
