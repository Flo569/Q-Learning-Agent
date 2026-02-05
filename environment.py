from logger import Logger
from settings import Settings
import copy

class Gridworld:

    def __init__(self, rows: int, columns: int, start: tuple, goal: tuple, walls: list[tuple], bonus: list[tuple]):

        self.steps: int = 0

        self.columns: int = columns
        self.rows: int = rows

        self.start_pos = start
        self.goal_pos = goal
        self.walls_pos = copy.deepcopy(walls)
        self.bonus_pos = copy.deepcopy(bonus)


    def reset(self):
        self.start_pos = Settings.start_pos
        self.goal_pos = Settings.goal_pos
        self.walls_pos = copy.deepcopy(Settings.wall_pos)
        self.bonus_pos = copy.deepcopy(Settings.bonus_pos)

        Settings.agent.reset(self.start_pos)
        self.steps = 0


    def train(self, episodes: int):

        if Settings.output_in_csv:
            Logger.init_logger()
            Logger.create_log_head()

        for i in range(episodes):
            self.reset()
            self.start_run(i+1)


    def start_run(self, episode: int):
        state = tuple(Settings.agent.position)         # initial state

        while True:
            self.steps += 1
            reward: int = 0
            done: bool = False
            success: bool = False

            # choose action, move and reward
            action: str = Settings.agent.choose_action(state)
            Settings.agent.move(action)
            reward += Settings.step_reward

            # check invalid action -> outside the world or wall
            x, y = Settings.agent.position
            if (x < 0 or x >= self.columns) or (y < 0 or y >= self.rows) or ((x, y) in self.walls_pos):
                reward += Settings.invalid_reward
                Settings.agent.position = state

            # check for bonus item
            elif (x, y) in self.bonus_pos:
                reward += Settings.bonus_reward
                self.bonus_pos.remove((x, y))           # remove item, only one-time-collectable

            # check for finishing the task
            elif self.goal_pos == (x, y):
                reward += Settings.goal_reward
                done = True
                success = True

            # update state and learn
            new_state = Settings.agent.position

            Settings.agent.score += reward

            if not done:
                Settings.agent.learn(state, action, reward, new_state)
                state = tuple(new_state)
            else:
                Settings.agent.terminal_learn(state, action, reward)

            # check for maximum steps
            if self.steps >= Settings.max_steps_per_episode:
                done = True
                success = False

            if done:
                if Settings.output_in_csv:
                    Logger.log_episode(episode, self.steps, Settings.agent.score, success, Settings.agent.epsilon_main,
                                       Settings.agent.q_table)
                break