import gym
from gym.envs.registration import register

register(
    id='RoboschoolPongSelfPlay-v0',
    entry_point='env.pong:RoboschoolPong',
    max_episode_steps=1000,
    tags={"pg_complexity": 20 * 1000000},
    kwargs={'self_play': True},
)

register(
    id='RoboschoolPong-v0',
    entry_point='env.pong:RoboschoolPong',
    max_episode_steps=1000,
    tags={"pg_complexity": 20 * 1000000},
)


def make_pong_env(self_play=False, player_n=0, seed=0, rank=0):
    if self_play:
        env = gym.make("RoboschoolPongSelfPlay-v0")
    else:
        env = gym.make("RoboschoolPong-v0")

    env.seed(seed + rank)
    return env