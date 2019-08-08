from roboschool.gym_pong import PongScene, PongSceneMultiplayer
from roboschool.gym_pong import RoboschoolPong as RoboschoolPong_
import numpy as np
import gym


class RoboschoolPong(RoboschoolPong_):

    def __init__(self, **kwargs):
        self.scene = None
        action_dim = 2
        obs_dim = 13
        high = np.ones([action_dim])
        self.action_space = gym.spaces.Box(-high, high)
        high = np.inf * np.ones([obs_dim])
        self.observation_space = gym.spaces.Box(-high, high)
        self.self_play = kwargs.get("self_play", False)
        self.seed()

    def create_single_player_scene(self):
        s = PongScene()
        s.np_random = self.np_random
        return s

    def create_multi_player_scene(self):
        s = PongSceneMultiplayer()
        s.np_random = self.np_random
        return s

    def reset(self):
        if self.scene is None:
            if self.self_play:
                self.scene = self.create_multi_player_scene()
            else:
                self.scene = self.create_single_player_scene()

        self.scene.episode_restart()

        if self.self_play:
            state_left = self.calc_state(0)
            state_right = self.calc_state(1)
            state = [state_left, state_right]
            self.score_reported_left = 0
            self.score_reported_right = 0
        else:
            state = self.calc_state(0)
            self.score_reported = 0
        return state

    def calc_state(self, player_n):
        j = self.scene.global_state()
        if player_n == 1:
            #                    [  0,1,  2,3,   4, 5, 6,7,  8,9,10,11,12]
            #                    [p0x,v,p0y,v, p1x,v,p1y,v, bx,v,by,v, T]
            signflip = np.array([-1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, 1])
            reorder = np.array([4, 5, 6, 7, 0, 1, 2, 3, 8, 9, 10, 11, 12])
            j = (j * signflip)[reorder]
        return j

    def apply_action(self, a):
        assert (np.isfinite(a).all())
        a = np.clip(a, -1, +1)
        if self.self_play:
            a0, a1 = a
            self.scene.p0x.set_target_speed(3 * float(a0[0]), 0.05, 7)
            self.scene.p0y.set_target_speed(3 * float(a0[1]), 0.05, 7)
            self.scene.p1x.set_target_speed(-3 * float(a1[0]), 0.05, 7)
            self.scene.p1y.set_target_speed(-3 * float(a1[1]), 0.05, 7)
        else:
            self.scene.p0x.set_target_speed(3 * float(a[0]), 0.05, 7)
            self.scene.p0y.set_target_speed(3 * float(a[1]), 0.05, 7)

    def step(self, a):
        self.apply_action(a)
        self.scene.global_step()

        if self.self_play:
            state_left = self.calc_state(0)
            state_right = self.calc_state(1)
            self.scene.HUD(a[0], state_left)

            new_score_left = self.scene.score_left
            rewards_left = [new_score_left - self.score_reported_left]
            self.score_reported_left = new_score_left

            new_score_right = self.scene.score_right
            rewards_right = [new_score_right - self.score_reported_right]
            self.score_reported_right = new_score_right

            return [state_left, state_right], [sum(rewards_left), sum(rewards_right)], False, {}

        else:
            state = self.calc_state(0)
            self.scene.HUD(a, state)

            new_score = self.scene.score_left
            self.rewards = [new_score - self.score_reported]
            self.score_reported = new_score

            return state, sum(self.rewards), False, {}
