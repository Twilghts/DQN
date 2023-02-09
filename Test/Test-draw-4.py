import copy

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Simhei']  # 显示中文
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

ospf_data = [(0.0134, 30000), (0.0283, 60000), (0.0442, 30000), (0.1191, 0), (0.3212, 30000), (0.3529, 0),
             (0.3531, 30000), (0.3694, 60000), (0.446, 30000), (0.4609, 60000), (0.5211, 30000), (0.5509, 0),
             (1.5899, 30000), (1.6539, 0)]

rip_data = [(0.0752, 30000), (0.1073, 0), (0.1542, 30000), (0.186, 0), (0.2323, 30000), (0.2645, 0), (0.2648, 30000),
            (0.2957, 0), (0.3728, 30000), (0.4042, 0), (0.4502, 30000), (0.5135, 60000),
            (0.606, 30000), (0.6512, 60000), (0.6659, 30000), (0.6661, 60000), (0.682, 30000), (0.7592, 0),
            (0.8069, 30000), (0.9002, 60000), (0.9952, 30000), (1.0595, 60000), (1.1832, 30000), (1.2473, 60000),
            (1.3891, 30000),
            (1.5972, 0)]

dqn_data = [(0.1297, 30000), (0.1552, 0), (0.1822, 30000), (0.2029, 0), (0.3278, 30000), (0.3595, 0), (0.7378, 30000),
            (0.7695, 0), (0.864, 30000), (0.8956, 0), (0.9912, 30000), (1.0222, 0), (1.0697, 30000), (1.1014, 0),
            (1.163, 30000), (1.1943, 0), (1.1986, 30000), (1.2262, 0)]

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
