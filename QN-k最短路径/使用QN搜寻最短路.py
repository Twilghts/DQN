import random
import time

import networkx as nx
import numpy as np


class QNetwork:
    def __init__(self, num_states, num_actions, learning_rate=0.01, discount_factor=0.9, epsilon=0.04):
        self.num_states = num_states
        self.num_actions = num_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

        self.q_table = np.zeros((num_states, num_actions))

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            # Explore: choose a random action
            action = np.random.randint(0, self.num_actions)
        else:
            # Exploit: choose the action with the highest Q value
            action = np.argmax(self.q_table[state, :])
        return action

    def choose_action_without_deviation(self, state):
        action = np.argmax(self.q_table[state, :])
        return action

    def update_q_table(self, state, action, reward, next_state):
        q_predict = self.q_table[state, action]
        q_target = reward + self.discount_factor * np.max(self.q_table[next_state, :])
        self.q_table[state, action] += self.learning_rate * (q_target - q_predict)


def shortest_path(graph, start, end, q_network, is_train=True):
    # Initialize variables
    state = start
    total_reward = 0
    steps = [start]

    # Keep looping until we reach the end node
    while state != end:
        # Choose an action using the Q-network
        if is_train:
            action = q_network.choose_action(state)
        else:
            action = q_network.choose_action_without_deviation(state)

        # Take the action and get the reward
        next_state, reward = graph[state][action]
        total_reward += reward
        if total_reward < -5000:
            break

        # Update the Q-table
        if is_train:
            q_network.update_q_table(state, action, reward, next_state)

        # Update the state
        state = next_state
        steps.append(state)

    return total_reward, steps


# Set the number of nodes and edges
n = 8
m = 36
# Find the 3 shortest paths between node 1 and node 5
k = 10

start_time = time.perf_counter()
# Generate the graph using the gnm_random_graph() function
G = nx.gnm_random_graph(n, m)
# Assign random weights to the edges
for u, v, d in G.edges(data=True):
    d['weight'] = random.randint(1, 100)

Graph = {u: [] for u in G.nodes}
for i in G.nodes:
    for j in range(len(G)):
        Graph[i].append((j, -G.get_edge_data(i, j, default={'weight': 3000})['weight']))

# Initialize the Q-network
q_network = QNetwork(num_states=len(Graph), num_actions=len(Graph))
# Find the shortest path between the _start and end nodes
start = 0
end = 4
max_rewords = -100000
best_steps = []
right_num = 0
# for i in range(2000):
#     reward, steps = shortest_path(graph, _start, end, q_network)
cost = nx.shortest_path_length(G, source=start, target=end, weight='weight')
path = nx.shortest_path(G, source=start, target=end)
print(path, cost)

for i in range(4000):
    reward, steps = shortest_path(Graph, start, end, q_network)

for j in range(100):
    reward, steps = shortest_path(Graph, start, end, q_network)
    max_rewords = reward
    best_steps = steps
    if reward > -1.1 * cost:
        right_num += 1

acc = right_num / 100
print(f"Shortest path from {start} to {end}: {best_steps}")
print(f"Total reward: {max_rewords}")
print(f"正确率: {acc}")
print(f"消耗时间: {time.perf_counter() - start_time}")
