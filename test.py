from env import make_pong_env


def test_single():
    env = make_pong_env(self_play=False)  # You can control left agent
    env.reset()
    while True:
        a = env.action_space.sample()  # Random Agent
        s, r, d, _ = env.step(a)
        env.render()
        if d:
            env.reset()


def test_multi():
    env = make_pong_env(self_play=True)  # Self-play mode, you can control both agents
    env.reset()
    for _ in range(10000):
        a = env.action_space.sample()  # Random Agent
        s, r, d, _ = env.step([a, a])
        env.render()
        if d:
            env.reset()


if __name__ == "__main__":
    test_single()
    # test_multi()
