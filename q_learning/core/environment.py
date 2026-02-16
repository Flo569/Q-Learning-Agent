from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from q_learning.core.agent import Agent

from q_learning.utils.logger import Logger
from q_learning.utils.settings import Settings
import copy


class Gridworld:

    def __init__(self, agent, rows: int, columns: int, start: tuple, goal: tuple, walls: list[tuple], bonus: list[tuple]):

        self.agent: Agent = agent
        self.steps: int = 0

        self.columns: int = columns
        self.rows: int = rows

        self.start_pos = start
        self.goal_pos = goal
        self.walls_pos = copy.deepcopy(walls)
        self.bonus_pos = copy.deepcopy(bonus)

        agent.init(self.rows, self.columns)


    def reset(self):
        self.start_pos = Settings.start_pos
        self.goal_pos = Settings.goal_pos
        self.walls_pos = copy.deepcopy(Settings.wall_pos)
        self.bonus_pos = copy.deepcopy(Settings.bonus_pos)

        self.agent.reset(self.start_pos)
        self.steps = 0


    def train(self, episodes: int):

        if Settings.output_in_csv:
            Logger.init_logger()
            Logger.create_log_head()

        for i in range(episodes):
            self.reset()
            self.start_run(i+1)

        # final run
        self.reset()
        self.agent.epsilon_main = 0
        self.agent.epsilon_min = 0
        self.start_run(episodes + 1)


    def start_run(self, episode: int):
        state = tuple((self.agent.position, self.agent.collected_mask))       # initial state

        while True:
            self.steps += 1
            reward: int = 0
            done: bool = False
            success: bool = False

            # choose action, move and reward
            action: str = self.agent.choose_action(state)
            self.agent.move(action)
            reward += Settings.step_reward

            # check invalid action -> outside the world or wall
            x, y = self.agent.position
            if (x < 0 or x >= self.columns) or (y < 0 or y >= self.rows) or ((x, y) in self.walls_pos):
                reward += Settings.invalid_reward
                self.agent.position, self.agent.collected_mask = state

            # check for bonus item
            elif (x, y) in self.bonus_pos:
                reward += Settings.bonus_reward
                self.agent.collected_mask += self.agent.bonus_pos_bit.get((x, y))
                self.bonus_pos.remove((x, y))           # remove item, only one-time-collectable

            # check for finishing the task
            elif self.goal_pos == (x, y):
                reward += Settings.goal_reward
                done = True
                success = True

            # update state and learn
            new_state = (self.agent.position, self.agent.collected_mask)

            self.agent.score += reward

            if done:
                self.agent.terminal_learn(state, action, reward)
            else:
                self.agent.learn(state, action, reward, new_state)
                state = tuple(new_state)

            # check for maximum steps
            if self.steps >= Settings.max_steps_per_episode:
                done = True
                success = False

            if Settings.output_detailed_log and Settings.output_in_csv:
                Logger.log_details(done, episode, state, action, reward, new_state)

            if done:
                if Settings.output_in_csv:
                    Logger.log_episode(episode, self.steps, self.agent.score, success,
                                       self.agent.epsilon_main, self.agent.q_table)
                break