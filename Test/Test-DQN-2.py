import random

import matplotlib.pyplot as plt
import torch
# from torch.distributed.argparse_util import env
import torch.nn as nn
import gym


def visualize_training(rewards):
    plt.plot(rewards)
    plt.xlabel('Episode')
    plt.ylabel('Total reward')
    plt.show()


class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, 32)
        self.fc2 = nn.Linear(32, 32)
        self.fc3 = nn.Linear(32, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def train_dqn(env, model, num_episodes):
    # Set up the optimizer and loss function
    optimizer = torch.optim.Adam(model.parameters())
    loss_fn = nn.MSELoss()

    # Set up the replay buffer
    replay_buffer = []
    replay_buffer_size = 10000

    rewards = []
    for episode in range(num_episodes):
        # Initialize the environment and state
        state = env.reset()
        total_reward = 0

        while True:
            # Select an action using the DQN model
            # action = model(torch.tensor(state, dtype=torch.float)).argmax().path()
            action = model.get

            # Take a step in the environment
            next_state, reward, done, _ = env.step(action)

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

