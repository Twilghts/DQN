import threading
import time

import matplotlib.pyplot as plt
import networkx as nx

from router import Router

# Set the number of nodes and edges
# n = 50  # 点的数量
# m = 150  # 边的数量
start = 1  # 起始点
target = 6  # 目标点

G = nx.Graph()
G.add_weighted_edges_from([(0, 1, 30), (0, 2, 45), (1, 2, 40), (1, 3, 10),
                           (2, 5, 20), (3, 4, 70), (4, 5, 25), (5, 7, 15),
                           (4, 8, 30), (7, 8, 20), (6, 7, 5), (6, 10, 20),
                           (8, 9, 15), (9, 10, 5)])

routers = {
    n: Router(n) for n in range(33)
}

path = nx.dijkstra_path(G, start, target)

# with open('Test_1.txt', 'r', encoding='utf-8') as f:
#     message = f.read()

if __name__ == '__main__':
    # print("准备发送信息")
    # times = []
    # routers[0].save(message)
    # for j in range(10):
    #     count = 1
    #     start_time = time.perf_counter()
    #     for i in range(32):
    #         print(f"经过的第{count}个路由器")
    #         Server_thread = threading.Thread(target=routers[i + 1].server_thread)
    #         Client_thread = threading.Thread(target=routers[i].client_thread, args=[routers[i + 1].get_port()])
    #         Server_thread.start()
    #         Client_thread.start()
    #         Server_thread.join()
    #         Client_thread.join()
    #         count += 1
    #         if not Client_thread.is_alive() and Server_thread.is_alive():
    #             continue
    #     print(f"消耗时间: {time.perf_counter() - start_time}")
    #     times.append(round(time.perf_counter() - start_time, 5))
    #
    # print(times)
    # # routers[_target].show()
    # print(f'最短路径{path}')
    # Draw the graph using the spring layout
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    #
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Show the plot
    plt.show()
