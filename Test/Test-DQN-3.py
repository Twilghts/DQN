import gym
from gym import envs

env_list = envs.registry.keys()
env_ids = [env_item for env_item in env_list]
print('There are {0} envs in gym'.format(len(env_ids)))
print(env_ids)

env = gym.make("Taxi-v3", render_mode="human")

class TimeLimit(gym.Wrapper):
    def __init__(self, env, max_episode_steps=None):
        super(TimeLimit, self).__init__(env)
        self._max_episode_steps = max_episode_steps
        self._elapsed_steps = 0

    def step(self, ac):
        o, r, done, *info, = self.env.step(ac)
        self._elapsed_steps += 1
        if self._elapsed_steps >= self._max_episode_steps:
            done = True
            info['TimeLimit.truncated'] = True
        return o, r, done, info

    def reset(self, **kwargs):
        self._elapsed_steps = 0
        return self.env.reset(**kwargs)


