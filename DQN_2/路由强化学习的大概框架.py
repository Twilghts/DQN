import networkx as nx
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

# Hyper Parameters
BATCH_SIZE = 32
LR = 0.01  # learning rate
EPSILON = 0.9  # greedy policy
GAMMA = 0.9  # reward discount
TARGET_REPLACE_ITER = 100  # 目标net更新频率
MEMORY_CAPACITY = 3000  # 经验池数量上限

# 将环境改成你们自己的路由环境
env = myenv()  # 主要是模拟路由转发的环境
# 路由转发的动作数量，即k最短路的k
N_ACTIONS = env.action_space.n
# 路由转发要使用的状态，即你们要保护的隐私数据。（可以参考：本路由器的数据缓存数量 或 本路由器缓存数量与相邻路由器的缓存数量）
N_STATES = env.observation_space.shape[0]


class Net(nn.Module):
    def __init__(self, ):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(N_STATES, 128)
        self.fc1.weight.data.normal_(0, 0.1)  # initialization
        self.fc2 = nn.Linear(128, 128)
        self.fc2.weight.data.normal_(0, 0.1)  # initialization
        self.out = nn.Linear(128, N_ACTIONS)
        self.out.weight.data.normal_(0, 0.1)  # initialization

    def forward(self, _x):
        _x = self.fc1(_x)
        _x = F.relu(_x)
        _x = self.fc2(_x)
        _x = F.relu(_x)
        actions_value = self.out(_x)
        return actions_value


class DQN(object):
    def __init__(self):
        self.eval_net, self.target_net = Net(), Net()

        self.learn_step_counter = 0  # for _target updating
        self.memory_counter = 0  # 经验池数量
        self.memory = np.zeros((MEMORY_CAPACITY, N_STATES * 2 + 2))  # 初始化经验池
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=LR)
        self.loss_func = nn.MSELoss()

    def choose_action(self, _x):
        _x = torch.unsqueeze(torch.FloatTensor(_x), 0)  # 在维度为0的位置加上一个维度
        # 选择价值最大的一个动作
        if np.random.uniform() < EPSILON:  # greedy
            actions_value = self.eval_net.forward(_x)
            action = torch.max(actions_value, 1)[1].data.numpy()
            action = action[0]  # return the argmax index
        else:  # random
            action = np.random.randint(0, N_ACTIONS)
            action = action
        return action

    def store_transition(self, _s, _a, _r, _s_):
        transition = np.hstack((_s, [_a, _r], _s_))
        # replace the old memory with new memory
        index = self.memory_counter % MEMORY_CAPACITY
        self.memory[index, :] = transition
        self.memory_counter += 1

    def learn(self):
        # 每学习一百次更新目标net
        if self.learn_step_counter % TARGET_REPLACE_ITER == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_step_counter += 1

        # 随机在经验池中选择一组batch
        sample_index = np.random.choice(MEMORY_CAPACITY, BATCH_SIZE)
        b_memory = self.memory[sample_index, :]
        b_s = torch.FloatTensor(b_memory[:, :N_STATES])
        b_a = torch.LongTensor(b_memory[:, N_STATES:N_STATES + 1].astype(int))
        b_r = torch.FloatTensor(b_memory[:, N_STATES + 1:N_STATES + 2])
        b_s_ = torch.FloatTensor(b_memory[:, -N_STATES:])

        # q_eval w.r.t the action in experience
        q_eval = self.eval_net(b_s).gather(1, b_a)  # 先通过eval_net根据b_s计算价值(一维)，然后通过gather选择指定动作的价值
        q_next = self.target_net(b_s_).detach()  # detach用来阻断反向传播(目标net不更新)
        q_target = b_r + GAMMA * q_next.max(1)[0].view(BATCH_SIZE, 1)  # resize (batch, 1)

        loss = self.loss_func(q_eval, q_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


# 获取k最短路径
# def init_shp_path(G):  # G是你们的网络拓扑
#     for i in range(node_num):  # 路由器节点数量
#         for j in range(node_num):
#             获取一条最短简单路
            # path = nx.shortest_simple_paths(G, source=i + 1, _target=j + 1, weight='delay')  # weight是边权，要你们自己设置
            # for counter, path in enumerate(path):
            #     保存k最短lu路径
                # shp_path[i][j].append(path)
                # if counter >= K - 1:
                #     break


if __name__ == '__main__':
    dqn = DQN()
    for i_episode in range(100000):  # 训练episode次数，可以自己调
        s = env.reset()  # 是你们路由环境里需要自己设置的方法函数
        reward = 0  # 累计奖励值
        while True:
            a = dqn.choose_action(s)  # 选择最短路中的一条
            # take action
            s_, r, done, info = env.step(a)

            # modify the reward
            x, x_dot, theta, theta_dot = s_  # 将状态拆分
            reward = 1  # 奖励值根据你们的网络环境自己设置

            dqn.store_transition(s, a, reward, s_)  # 作为一组转变存入经验池

            # 首先需要将经验池装满，装满后开始学习
            if dqn.memory_counter > MEMORY_CAPACITY:
                dqn.learn()
            s = s_
