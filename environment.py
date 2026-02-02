from settings import Settings

class Gridworld:

    def __init__(self, rows: int, columns: int, start: tuple[int, int], goal: tuple[int, int],
                 walls: list[tuple[int, int]], bonus: list[tuple[int, int]]):

        self.steps: int = 0

        self.columns: int = columns
        self.rows: int = rows

        self.start_pos = start
        self.goal_pos = goal
        self.walls_pos = walls
        self.bonus_pos = bonus


    def reset(self):
        Settings.agent.reset(self.start_pos)
        self.steps = 0


    def train(self, episodes: int):
        for i in range(episodes):
            self.reset()
            self.start_run()


    def start_run(self):
        state = Settings.agent.position         # initial state

        while True:
            self.steps += 1
            reward: int = 0
            done: bool = False

            # choose action, move and reward
            action = Settings.agent.choose_action(state)
            Settings.agent.move(action)
            reward += Settings.step_reward

            # check invalid action -> outside the world or wall
            x, y = Settings.agent.position
            if (x < 0 or x >= self.columns) or (y < 0 or y >= self.rows) or (self.walls_pos.__contains__((x, y))):
                reward += Settings.invalid_reward
                Settings.agent.position = state

            # check for bonus item
            if self.bonus_pos.__contains__((x, y)):
                reward += Settings.bonus_reward
                self.bonus_pos.remove((x, y))           # remove item, only one-time-collectable

            # check for finishing the task
            if self.goal_pos == (x, y):
                reward += Settings.goal_reward
                done = True

            # update state and learn
            new_state = Settings.agent.position

            Settings.agent.learn(state, action, reward, new_state)
            state = new_state

            # check for maximum steps
            if self.steps == Settings.max_steps_per_episode:
                done = True

            if done:
                print('Score: ', Settings.agent.score, "\n Steps:", self.steps)
                break