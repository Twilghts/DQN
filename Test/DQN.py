import collections
import random

import gym
import matplotlib.pyplot as plt
import numpy as np
import tensorflow
import torch
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam
from torch import nn


def visualize_training(rewards):
    plt.plot(rewards)
    plt.xlabel('Episode')
    plt.ylabel('Total reward')
    plt.show()


class DQN:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = collections.deque(maxlen=2000)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Build the neural network to approximate the Q-function
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * \
                         np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def train_dqn(env, model, num_episodes):
    # Set up the optimizer and loss function
    optimizer = tensorflow.optimizers.Adam(learning_rate=0.95, epsilon=1e-5)
    loss_fn = nn.MSELoss()

    # Set up the replay buffer
    replay_buffer = []
    replay_buffer_size = 10000

    rewards = []
    for episode in range(num_episodes):
        # Initialize the environment and state
        state = env.reset()
        total_reward = 0
        for i in range(100):
            action = model.act(state)
            next_state, reward, done, *_ = env.step(action)
            replay_buffer.append((state, action, reward, next_state, done))

        while True:
            # Select an action using the DQN model
            # action = model(torch.tensor(state, dtype=torch.float)).argmax().path()
            action = model.act(state)

            # Take a step in the environment
            next_state, reward, done, *_ = env.step(action)

            # Store the transition in the replay buffer
            replay_buffer.append((state, action, reward, next_state, done))
            if len(replay_buffer) > replay_buffer_size:
                replay_buffer.pop(0)

            # Sample a batch of transitions from the replay buffer
            samples = random.sample(replay_buffer, 32)
            states, actions, rewards, next_states, dones = zip(*samples)

            # Calculate the Q-values for the next states
            next_q_values = model(torch.tensor(next_states, dtype=torch.float)).max(dim=1)[0]

            # Set the _target Q-values for the current states
            targets = torch.tensor(rewards, dtype=torch.float) + 0.99 * next_q_values * (
                    1 - torch.tensor(dones, dtype=torch.float))

            # Calculate the Q-values for the current states
            q_values = model(torch.tensor(states, dtype=torch.float)).gather(1, torch.tensor(actions).view(-1, 1)).view(
                -1)

            # Calculate the loss
            loss = loss_fn(q_values, targets)

            # Perform backpropagation and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_reward += reward
            state = next_state

            if done:
                rewards.append(total_reward)
                visualize_training(rewards)
                break


# Create an instance of the CartPole-v1 environment
env = gym.make('CartPole-v1')

# Get the shape of the observation space
input_size = env.observation_space.shape[0]

# Get the number of actions available in the environment
output_size = env.action_space.n
model = DQN(input_size, output_size)

# Create the _target model
target_model = DQN(input_size, output_size)

num_episodes = 1000
train_dqn(env, model, num_episodes)
