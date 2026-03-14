import random
from q_learning.utils.settings import Settings

class Agent:

    def __init__(self):

        self.q_table: dict = {}
        self.actions: list = ["up", "down", "left", "right"]

        self.collected_mask: int = 0
        self.bonus_pos_bit: dict = {}

        # default values
        self.position: tuple = (0, 0)      # (x, y)
        self.score: int = 0
        self.steps: int = 0

        self.alpha: float = 0
        self.gamma: float = 0
        self.epsilon_main: float = 0
        self.epsilon_decay: float = 0
        self.epsilon_min: float = 0


    # Resets Agent to start-values after the maze changed
    def init(self, rows: int, columns: int):

        self.position = Settings.start_pos
        self.collected_mask: int = 0
        self.bonus_pos_bit: dict = {}

        self.score = 0
        self.steps = 0

        self.alpha = Settings.alpha
        self.gamma = Settings.gamma
        self.epsilon_main = Settings.epsilon_main
        self.epsilon_decay = Settings.epsilon_decay
        self.epsilon_min = Settings.epsilon_min

        for x in range(columns):
            for y in range(rows):
                for action in self.actions:
                    self.q_table[((x, y), action)] = 0

        for bonus in Settings.bonus_pos:
            self.bonus_pos_bit[bonus] = 2**(Settings.bonus_pos.index(bonus))


    # Resets the agent everytime he ends a run
    def reset(self, start_pos):
        self.score = 0
        self.steps = 0
        self.collected_mask = 0
        self.position = start_pos
        self.epsilon_main *= max(self.epsilon_decay, self.epsilon_min)


    def choose_action(self, state: tuple):

        if random.random() < self.epsilon_main:             # random based on epsilon_main
            return random.choice(self.actions)

        else:
            q_values = []

            for action in self.actions:                     # get q_value for each action
                key = (state, action)
                q = self.q_table.get(key, 0)
                q_values.append((q, action))

            max_q = max(q_values, key=lambda x : x[0])[0]               # searches the highest value
            best_action = [a for (q, a) in q_values if q == max_q]      # choose action based on highest value

            return random.choice(best_action)               # choose one of the best actions


    def learn(self, state: tuple, action: str, reward: int, new_state: tuple):
        key = (state, action)
        current_q = self.q_table.get(key, 0)
        max_future_q = max([self.q_table.get((new_state, a), 0) for a in self.actions])
        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
        self.q_table[key] = new_q


    # learn without future-prediction -> cause last learn
    def terminal_learn(self, state: tuple, action: str, reward: int):
        key = (state, action)
        current_q = self.q_table.get(key, 0)
        new_q = current_q + self.alpha * (reward - current_q)
        self.q_table[key] = new_q


    # changes (x, y) based on action
    def move(self, action: str):
        x, y = self.position

        if action == "up":
            y -= 1
        elif action == "down":
            y += 1
        elif action == "left":
            x -= 1
        elif action == "right":
            x += 1

        self.position = (x, y)