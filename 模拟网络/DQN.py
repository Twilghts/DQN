import random
from collections import deque

import numpy as np
import tensorflow as tf


class DQN:
    def __init__(self, state_size, action_size):
        self.state_size: int = state_size
        self.action_size: int = action_size
        self.memory: deque = deque(maxlen=2000)
        self.gamma: float = 0.95  # 折扣率
        self.epsilon: float = 1.0  # 随机探索率
        self.epsilon_min: float = 0.001  # 最低随机探索率
        self.epsilon_decay: float = 0.995  # 探索率下降指数
        self.learning_rate: float = 0.01  # 学习率
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

    def choose_path(self, paths, is_best=False):
        #  进行探索
        #  随机探索
        if np.random.rand() <= self.epsilon and not is_best:
            return random.choice([path for path in paths])  # 返回随机路径
        #  根据模型取最优行为
        values: dict = {}  # 该字典的键为每条路径的预期奖励值，值为该奖励值所对应的路径
        for _path in paths:
            """为每条路径算出预期奖励值"""
            value: float = 0
            for i in range(len(_path) - 1):
                value += self.model(np.array([_path[i]])).numpy()[0][_path[i + 1]]
            values[value] = _path
        """通过每条路径奖励值的大小选择最佳路径"""
        path: list = max([_item for _item in values.items()],
                         key=lambda x: x[0])[1]
        return path

    def replay(self, batch_size, graph):
        #  取小批量数据优化模型
        minibatch: list = random.sample(self.memory, batch_size)
        for _state, _action, reward, _next_state, done in minibatch:
            target: float = reward
            target_f: list = self.model(np.array([_state])).numpy()  # 当前状态下的所有预测值
            if not done:
                """下一个状态下的所有预测值，并计算下一个状态下所有action带来的奖励中最低的"""
                values: list = self.model(np.array([_next_state])).numpy()
                target: float = reward + self.gamma * min(
                    [values[0][next_s] for next_s, a in graph[_next_state].items()])
            target_f[0][_action]: float = target
            self.model.fit(np.array([_state]), target_f, epochs=1, verbose=0)
        #  降低随机探索的概率
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
