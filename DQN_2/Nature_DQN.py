import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import gym
import time

# Hyper Parameters
BATCH_SIZE = 32
LR = 0.01                   # learning rate
EPSILON = 0.9               # greedy policy
GAMMA = 0.9                 # reward discount
TARGET_REPLACE_ITER = 100   # 目标net更新频率
MEMORY_CAPACITY = 3000      # 经验池数量上限
env = gym.make('CartPole-v0')
env = env.unwrapped
N_ACTIONS = env.action_space.n
N_STATES = env.observation_space.shape[0]
ENV_A_SHAPE = 0 if isinstance(env.action_space.sample(), int) else env.action_space.sample().shape     # to confirm the shape


class Net(nn.Module):
    def __init__(self, ):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(N_STATES, 128)
        self.fc1.weight.data.normal_(0, 0.1)   # initialization
        self.fc2 = nn.Linear(128, 128)
        self.fc2.weight.data.normal_(0, 0.1)  # initialization
        self.out = nn.Linear(128, N_ACTIONS)
        self.out.weight.data.normal_(0, 0.1)   # initialization

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        actions_value = self.out(x)
        return actions_value


class DQN(object):
    def __init__(self):
        self.eval_net, self.target_net = Net(), Net()

        self.learn_step_counter = 0                                     # for _target updating
        self.memory_counter = 0                                         # 经验池数量
        self.memory = np.zeros((MEMORY_CAPACITY, N_STATES * 2 + 2))     # 初始化经验池
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=LR)
        self.loss_func = nn.MSELoss()

    def choose_action(self, x):
        x = torch.unsqueeze(torch.FloatTensor(x), 0)        # 在维度为0的位置加上一个维度
        # 选择价值最大的一个动作
        if np.random.uniform() < EPSILON:   # greedy
            actions_value = self.eval_net.forward(x)
            action = torch.max(actions_value, 1)[1].data.numpy()
            action = action[0] if ENV_A_SHAPE == 0 else action.reshape(ENV_A_SHAPE)  # return the argmax index
        else:   # random
            action = np.random.randint(0, N_ACTIONS)
            action = action if ENV_A_SHAPE == 0 else action.reshape(ENV_A_SHAPE)
        return action

    def store_transition(self, s, a, r, s_):
        transition = np.hstack((s, [a, r], s_))
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
        b_a = torch.LongTensor(b_memory[:, N_STATES:N_STATES+1].astype(int))
        b_r = torch.FloatTensor(b_memory[:, N_STATES+1:N_STATES+2])
        b_s_ = torch.FloatTensor(b_memory[:, -N_STATES:])

        # q_eval w.r.t the action in experience
        q_eval = self.eval_net(b_s).gather(1, b_a)  # 先通过eval_net根据b_s计算价值(一维)，然后通过gather选择指定动作的价值
        q_next = self.target_net(b_s_).detach()     # detach用来阻断反向传播(目标net不更新)
        q_target = b_r + GAMMA * q_next.max(1)[0].view(BATCH_SIZE, 1)   # resize (batch, 1)

        # print(q_eval.shape)
        # print(q_next.shape)
        # print(q_target.shape)
        # print(q_target)
        # time.sleep(20)

        loss = self.loss_func(q_eval, q_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

start_time = time.perf_counter()
dqn = DQN()
num_600 = 0

print('\nCollecting experience...')
for i_episode in range(500):
    s = env.reset()         # 四个状态[x轴位置,x轴加速度,杆子角度,杆子加速度]
    ep_r = 0                # 累计奖励
    while True:
        env.render()
        a = dqn.choose_action(s)    # 两个动作[左移,右移]
        # take action
        s_, r, done, info = env.step(a)

        # modify the reward
        x, x_dot, theta, theta_dot = s_     # 将状态拆分
        r1 = (env.x_threshold - abs(x)) / env.x_threshold - 0.8                                 # x轴坐标的奖励函数
        r2 = (env.theta_threshold_radians - abs(theta)) / env.theta_threshold_radians - 0.5     # 杆子角度的奖励函数
        r = r1 + r2

        dqn.store_transition(s, a, r, s_)           # 作为一组转变存入经验池

        ep_r += r           # 累计奖励
        # 首先需要将经验池装满，装满后开始学习
        if dqn.memory_counter > MEMORY_CAPACITY:
            dqn.learn()
            if done:
                print('Ep: ', i_episode,
                      '| Ep_r: ', round(ep_r, 2))
            if ep_r > 400:
                done = 1
                break
        if done:
            break
        s = s_
    if ep_r > 400 and num_600 > 2:
        torch.save(dqn, 'ndqn.pt')
        break
    elif ep_r > 400:
        num_600 += 1
print(f'消耗时间:{time.perf_counter() - start_time}')