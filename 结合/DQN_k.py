import time

import matplotlib.pyplot as plt
import networkx as nx
import tensorflow as tf
import numpy as np
from 模拟网络.DQN import DQN
from 模拟网络.K最短路径算法 import k_shortest_paths

# Set the number of nodes and edges
n = 12
m = 18
# Find the 3 shortest paths between node 1 and node 5
start = 1
goal = 7
_k = 3  # k最短路径的总数

# G = nx.read_gexf('Graph_1')  # 读取图的信息
G = nx.Graph()
G.add_weighted_edges_from([(0, 1, 35), (0, 2, 30), (1, 2, 20), (1, 3, 25),
                           (2, 5, 20), (3, 4, 70), (4, 5, 25), (5, 7, 15),
                           (4, 8, 30), (7, 8, 20), (6, 7, 5), (6, 10, 20),
                           (8, 9, 15), (9, 10, 5)])

dqn_agent = DQN(1, len(G.nodes()))
dqn_agent.model = tf.keras.models.load_model('model_3.h5')  # 读取模型的信息

if __name__ == '__main__':
    start_time = time.perf_counter()
    print(f'起始时间为', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # for i in range(1000):
    #     number = 0
    #     state = _start
    #     while state != goal:
    #         number += 1
    #         if number >= 100:
    #             break
    #         action = dqn_agent.act(state, G)  # act行为带来一次预测
    #         weight = G[state][action]['weight']
    #         next_state = action
    #         dqn_agent.remember(state, action, -weight, next_state, next_state == goal)
    #         state = next_state
    #     if len(dqn_agent.memory) >= 36:
    #         dqn_agent.replay(36, G)  # 一次优化模型行为带来2次预测，共带来72次预测
    #     print(f'第{i + 1}次训练模型。')

    P = k_shortest_paths(G, start, goal, _k)

    values = {}  # 该字典的键为每条路径的预期奖励值，值为该奖励值所对应的路径
    for _path in P:
        """为每条路径算出预期奖励值"""
        value = 0
        for i in range(len(_path) - 1):
            value += dqn_agent.model(np.array([_path[i]])).numpy()[0][_path[i + 1]]
        values[value] = _path
    """通过每条路径奖励值的大小选择最佳路径"""
    path = max([_item for _item in values.items()],
               key=lambda x: x[0])[1]

    print(f"使用k最短路径算法算出来的最短路径群:{P}")
    for item in values.items():
        print(f'路径{item[1]}的总奖励为{item[0]}')
    print(f'迪杰斯特拉算法推荐的最佳路径为{nx.dijkstra_path(G, start, goal)}')
    print(f'DQN算法推荐的最优路径{path}')
    print(f"消耗时间:{time.perf_counter() - start_time}")
    print(f'起始时间为', start_time_str)
    print(f'终止时间为', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    # dqn_agent.model.save('model_3.h5')  # 保存模型的信息
    # nx.write_gexf(G, 'Graph_1')  # 保存图的信息

    # 使用spring布局绘制图形
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)

    # 添加显示权重的边标签
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # 显示绘图
    plt.show()
