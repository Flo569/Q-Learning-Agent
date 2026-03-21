from __future__ import annotations

import os
import copy

from q_learning.tools.visualizer import Visualizer
from q_learning.utils.logger import Logger
from q_learning.utils.settings import Settings
from q_learning.utils.settings import implement_layout

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from q_learning.core.agent import Agent


class Gridworld:

    def __init__(self, agent, visualizer: Visualizer | None = None):

        self.agent: Agent = agent
        self.visualizer = visualizer

        self.columns: int = Settings.columns
        self.rows: int = Settings.rows

        self.start_pos = None
        self.goal_pos = None
        self.walls_pos = None
        self.bonus_pos = None

        self.trail: list = []


    # resets environment and agent for a new run
    def reset(self):
        self.columns = Settings.columns
        self.rows = Settings.rows
        self.start_pos = Settings.start_pos
        self.goal_pos = Settings.goal_pos
        self.walls_pos = copy.deepcopy(Settings.wall_pos)
        self.bonus_pos = copy.deepcopy(Settings.bonus_pos)

        self.agent.reset(self.start_pos)


    def train(self, episodes: int):

        self.reset()

        if self.visualizer:
            self.visualizer.start()

        if Settings.output_in_csv:
            Logger.init_logger()

        files: list = sorted(os.listdir(f"mazes/{Settings.maze_directory}"))
        for filename in files:                              # train for every maze
            implement_layout(filename)                      # load maze
            Logger.log_layout(filename)                     # update logger

            self.reset()
            self.agent.init(self.rows, self.columns)        # reset agent to default values

            if self.visualizer:
                self.visualizer.init(filename)

            print(f"Start solving {filename}!")

            # training
            for i in range(episodes):

                if i % (episodes*0.1) == 0:
                    print(f"{i/episodes * 100}% solved!")

                self.reset()
                self.start_run(i+1, filename)

            print(f"{filename} completed!")

            # final run
            self.reset()
            self.agent.epsilon_main = 0
            self.agent.epsilon_min = 0
            self.start_run(episodes+1, filename)

            Logger.reset()

        Logger.final_log()
        if self.visualizer:
            self.visualizer.shutdown()


    def start_run(self, episode: int, filename: str):

        self.trail = []
        state = tuple(self.agent.position)         # initial state – (x, y)

        while True:

            if self.visualizer:
                self.visualizer.pause()

            self.agent.steps += 1
            reward: int = 0
            done: bool = False
            success: bool = False

            # choose action, move and reward
            action: str = self.agent.choose_action(state)
            self.agent.move(action)
            reward += Settings.step_reward

            self.trail.append(list(self.agent.position))

            # check invalid action -> outside the world or wall
            x, y = self.agent.position
            if (x < 0 or x >= self.columns) or (y < 0 or y >= self.rows) or ((x, y) in self.walls_pos):
                reward += Settings.invalid_reward
                self.agent.position = state

            # check for bonus item
            elif (x, y) in self.bonus_pos:
                reward += Settings.bonus_reward
                self.bonus_pos.remove((x, y))           # remove item; only one-time-collectable

            # check for finishing the task
            elif self.goal_pos == (x, y):
                reward += Settings.goal_reward
                done = True
                success = True

            # update state and learn
            new_state = self.agent.position

            self.agent.score += reward

            if done:
                self.agent.terminal_learn(state, action, reward)                # final learn process -> no future steps
            else:
                self.agent.learn(state, action, reward, new_state)
                state = tuple(new_state)

            # check for maximum steps
            if self.agent.steps >= Settings.max_steps_per_episode:
                done = True
                success = False

            # log this run
            if Settings.output_in_csv:
                Logger.log_details(filename, done, episode, state, action, reward, new_state, self.agent.q_table)

            # visualizer
            if self.visualizer:
                self.visualizer.update(
                    self.agent.position,
                    episode,
                    self.agent.steps,
                    self.agent.epsilon_main,
                    reward,
                    self.agent.score,
                    self.bonus_pos,
                    self.trail,
                    done,
                    success
                )


            if done:
                if Settings.output_in_csv:
                    Logger.log_episode(episode, self.agent.steps, self.agent.score, success, self.agent.epsilon_main)
                break
