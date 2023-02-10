import copy

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Simhei']  # 显示中文
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

ospf_data = [(0.4015, 2000), (0.4936, 0), (1.1436, 2000), (1.2363, 0), (1.2364, 2000), (1.3304, 0), (1.5176, 2000),
             (1.5784, 4000), (1.6091, 2000), (1.6707, 0), (1.8421, 2000), (1.9355, 0), (1.9965, 2000), (2.0887, 0),
             (2.2938, 2000), (2.3877, 0), (2.9757, 2000), (3.0681, 4000), (3.0686, 2000), (3.1616, 0), (3.1618, 2000),
             (3.2547, 0), (3.471, 2000), (3.5631, 0), (3.7506, 2000), (3.8427, 0), (4.0302, 2000), (4.1247, 0),
             (5.1776, 2000), (5.2724, 4000), (5.3025, 2000), (5.3945, 0)]

rip_data = [(0.3076, 2000), (0.4009, 0), (0.4014, 2000), (0.4929, 0), (0.9124, 2000), (0.9742, 4000), (1.0062, 2000),
            (1.0675, 0), (1.1456, 2000), (1.2245, 4000), (1.2405, 2000), (1.3016, 4000),
            (1.3178, 2000), (1.3635, 4000), (1.3958, 2000), (1.5192, 0), (2.2312, 2000), (2.3251, 0), (2.4174, 2000),
            (2.4813, 4000), (2.5122, 2000), (2.5743, 0), (2.7443, 2000), (2.837, 0), (2.9465, 2000), (3.0377, 0),
            (3.0985, 2000), (3.1908, 0), (3.4088, 2000), (3.5455, 4000), (3.5607, 2000), (3.6384, 0), (3.7316, 2000),
            (3.8236, 0), (3.8397, 2000), (3.9317, 0), (4.0538, 2000), (4.0982, 4000), (4.1453, 2000),
            (4.2542, 0), (4.3188, 2000), (4.4104, 0), (4.7369, 2000), (4.8918, 0)]

dqn_data = [(1.1918, 2000), (1.285, 0), (1.3169, 2000), (1.3934, 4000), (1.408, 2000), (1.486, 0), (1.6412, 2000),
            (1.7041, 4000), (1.734, 2000), (1.7643, 4000), (1.8565, 2000), (1.9808, 0), (2.0422, 2000), (2.1363, 0),
            (2.3546, 2000), (2.4159, 4000), (2.4462, 2000), (2.477, 4000), (2.5078, 2000), (2.5686, 0), (2.9123, 2000),
            (3.0048, 4000), (3.0048, 2000), (3.0674, 4000), (3.0988, 2000), (3.1601, 0), (3.1602, 2000), (3.2531, 0),
            (3.2851, 2000), (3.3782, 0), (3.6109, 2000), (3.7028, 0), (3.7626, 2000), (3.8552, 0), (3.9479, 2000),
            (4.042, 0), (4.1672, 2000), (4.2435, 4000), (4.2594, 2000), (4.3065, 4000), (4.3374, 2000), (4.3979, 0),
            (4.5837, 2000), (4.735, 0)]

ospf_data.insert(0, (0, 0))
rip_data.insert(0, (0, 0))
dqn_data.insert(0, (0, 0))

ospf_view = copy.deepcopy(ospf_data)
rip_view = copy.deepcopy(rip_data)
dqn_view = copy.deepcopy(dqn_data)

for i in range(len(ospf_data) - 1):
    auxiliary_point = (ospf_data[i + 1][0], ospf_data[i][1])
    ospf_view.insert(2 * i + 1, auxiliary_point)

for i in range(len(rip_data) - 1):
    auxiliary_point = (rip_data[i + 1][0], rip_data[i][1])
    rip_view.insert(2 * i + 1, auxiliary_point)

for i in range(len(dqn_data) - 1):
    auxiliary_point = (dqn_data[i + 1][0], dqn_data[i][1])
    dqn_view.insert(2 * i + 1, auxiliary_point)

ospf_x = [i[0] for i in ospf_view]
ospf_y = [i[1] for i in ospf_view]

rip_x = [i[0] for i in rip_view]
rip_y = [i[1] for i in rip_view]

dqn_x = [i[0] for i in dqn_view]
dqn_y = [i[1] for i in dqn_view]

plt.plot(ospf_x, ospf_y, color='red', label='OSPF')
plt.plot(rip_x, rip_y, color='wheat', label='RIP')
plt.plot(dqn_x, dqn_y, color='aquamarine', label='DQN')

plt.xlim(0, max([ospf_view[-1][0], rip_view[-1][0], dqn_view[-1][0]]) * 1.1)
plt.ylim(0, max([item[1] for sublist in [ospf_view, rip_view, dqn_view] for item in sublist]) * 1.1)
plt.xlabel('时间')
plt.ylabel('吞吐量')
plt.title('一个路由器的吞吐量随时间变化的关系。')
plt.legend()
# Save the plot as an SVG
plt.savefig("plot.svg")
plt.show()
