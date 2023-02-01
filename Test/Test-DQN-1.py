import matplotlib.pyplot as plt

# ...
import gym
from DQN import DQN
import numpy as np

env = gym.make('CartPole-v1')
state_size = env.observation_space.shape[0]
action_size = env.action_space.n
agent = DQN(state_size, action_size)

done = False
batch_size = 32
# Create two empty lists to store the scores and epsilon values
scores = []
epsilons = []
EPISODES = 100

for e in range(EPISODES):
    state = env.reset()
    state = np.reshape(state, [1, state_size])
    score = 0
    for time in range(500):
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        reward = reward if not done else -10
        next_state = np.reshape(next_state, [1, state_size])
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        score += reward
        if done:
            scores.append(score)
            epsilons.append(agent.epsilon)
            break
    if len(agent.memory) > batch_size:
        agent.replay(batch_size)

# Plot the scores over time
plt.plot(scores)
plt.xlabel('Episode')
plt.ylabel('Score')
plt.show()

# Plot the epsilon values over time
plt.plot(epsilons)
plt.xlabel('Episode')
plt.ylabel('Epsilon')
plt.show()
