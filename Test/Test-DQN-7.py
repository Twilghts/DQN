import gym

env = gym.make('Pendulum-v1', render_mode="human")
initialization = env.reset()
while True:
    env.render()
    # 随机选择动作
    a = env.action_space.sample()
    o, r, done, *_ = env.step(a)
    print(f'{env.step(a)}')
    if done:
        break
env.close()
