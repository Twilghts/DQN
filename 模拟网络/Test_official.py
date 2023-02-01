import threading
import time

from ospf_network import Ospf

if __name__ == '__main__':
    print(f'起始时间为', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    ospf_net = Ospf()  # 实例化OSPF网络
    thread_pool = []  # 线程池
    start_time = time.perf_counter()  # 计算起始时间
    ospf_net.time = start_time  # 更新网络开始时的时间戳，为计算吞吐量做准备
    """正式启动信息发送"""
    for data in ospf_net.data_set:
        task_thread = threading.Thread(target=ospf_net.send_message, args=[data, False])  # 为每一个发送信息的过程创建线程
        print(f'线程{task_thread.name}开启!')
        task_thread.start()  # 启动线程
        thread_pool.append(task_thread)  # 将线程添加到线程池
        time.sleep(0.005)  # 每隔0.005秒发送一个数据包
    """测试所有的线程是否存活，如果所有线程都结束运行，则主线程继续运行"""
    while True:
        for thread in thread_pool:
            """如果线程结束，从线程池中移除该线程，并打印出相关性息!"""
            if not thread.is_alive():
                thread_pool.remove(thread)
                print(f'线程{thread.name}结束运行')
        """如果线程池被清空，则继续运行!"""
        if len(thread_pool) == 0:
            break
    end_time = time.perf_counter()
    for router in ospf_net.routers.values():
        print(f'路由器:{router.sign},吞吐量:{router.handling_capacity}')

    gross = 0  # 数据包总量
    failure = 0  # 成功的数据包数量
    for log in ospf_net.logs.items():
        print(f'数据包:{log[0]},数据记录:{log[1]}')
        gross += 1
        if not log[1][-1]:
            failure += 1
    print(f'丢包率:{round(failure / gross * 100, 3)}%')  # 保留三位小数
    print(f'消耗时间:{end_time - start_time}')
    print(f'终止时间为', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    ospf_net.show_graph()
