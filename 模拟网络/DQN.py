import random
from collections import deque

import numpy as np
import tensorflow as tf


class DQN:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # 折扣率
        self.epsilon = 1.0  # 随机探索率
        self.epsilon_min = 0.01  # 最低随机探索率
        self.epsilon_decay = 0.95  # 探索率下降指数
        self.learning_rate = 0.001  # 学习率
        self.model = self._build_model()  # 建造模型

    def _build_model(self):
        # 用于深度q学习模型的神经网络
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(48, input_dim=self.state_size, activation='relu'))
        model.add(tf.keras.layers.Dense(48, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, _state, _action, reward, _next_state, done):
        #  储存回放缓存
        self.memory.append((_state, _action, reward, _next_state, done))

    def act(self, _state, graph):
        #  进行探索
        #  随机探索
        if np.random.rand() <= self.epsilon:
            return random.choice([_action for _action in graph.neighbors(_state)])  # 返回随机动作
        #  根据模型取最优行为
        act_values = self.model(np.array([_state])).numpy()
        return max([_action for _action in graph.neighbors(_state)],
                   key=lambda x: act_values[0][x])  # 以最小估计距离返回动作

    def replay(self, batch_size, graph):
        #  取小批量数据优化模型
        minibatch = random.sample(self.memory, batch_size)
        for _state, _action, reward, _next_state, done in minibatch:
            target = reward
            target_f = self.model(np.array([_state])).numpy()  # 当前状态下的所有预测值
            if not done:
                """下一个状态下的所有预测值，并计算下一个状态下所有action带来的奖励中最低的"""
                values = self.model(np.array([_next_state])).numpy()
                target = reward + self.gamma * min(
                    [values[0][next_s] for next_s, a in graph[_next_state].items()])
            target_f[0][_action] = target
            self.model.fit(np.array([_state]), target_f, epochs=1, verbose=0)
        #  降低随机探索的概率
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
