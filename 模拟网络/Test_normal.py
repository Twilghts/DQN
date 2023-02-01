import collections
import random

import networkx as nx
import numpy

from data import Data
from net import Net
from dqn_network import DqnNetworkAgent
from 利用network实现k最短路径算法 import k_shortest_paths

n = 50  # 点的数量
m = 75  # 边的数量
for i in range(10):
    print(random.randint(0, 10))

G = nx.gnm_random_graph(n, m)
# Assign random weights to the edges
for u, v, d in G.edges(data=True):
    d['weight'] = random.randint(1, 100)

data_set = {Data(x, y, False) for x, y in zip(numpy.random.choice(G.nodes, 100), numpy.random.choice(G.nodes, 100)) if x == y}
print(data_set)
print(f'图的点为{G.nodes}')
print(f'图的点为{numpy.random.choice(G.nodes)}')
print(numpy.random.choice(G.nodes))


class TestNet(Net):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    test_net = TestNet()
    print(test_net.links)
    print(test_net.routers)
    print(test_net.data_set)
    for router in test_net.routers.values():
        print(router.routing_table)

    print((0, 0) != (1, 0) and (1, 0) != (0, 1))
    for i in range(10):
        # print(i)
        if i > 5:
            break
    deque_1 = collections.deque(maxlen=1000)
    list_1 = [i for i in range(10)]
    set_1 = set(list_1)
    # print(list_1[-1])
    # for i in set_1:
    #     print(i)
    list_2 = [[i for i in range(10)], 2]
    list_3 = [[i for i in range(10, 20)], 3]
    list_4 = []
    print(len(list_4))
    dict_1 = {
        key: value for key, value in zip(random.sample(list_1, 5), random.sample(list_1, 5))
    }
    for item in dict_1.items():
        print(f'key:{item[0]},value:{item[1]}')
    dqn_net_agent = DqnNetworkAgent()
    print(dqn_net_agent.memory)
    dqn_net_agent.show_graph()
    print(k_shortest_paths(dqn_net_agent.G, 7, 9, 1))

