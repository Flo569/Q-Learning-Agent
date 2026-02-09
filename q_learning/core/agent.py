import random
from q_learning.utils.settings import Settings

class Agent:

    def __init__(self, alpha: float, gamma: float, epsilon_main: float, epsilon_decay: float, epsilon_min: float):

        self.position = Settings.start_pos

        self.score = 0

        self.q_table = {}
        self.actions = ["up", "down", "left", "right"]

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_main = epsilon_main
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min


    def init(self, rows: int, columns: int):
        for x in range(columns):
            for y in range(rows):
                for action in self.actions:
                    self.q_table[((x, y), action)] = 0


    def reset(self, start_pos):
        self.score = 0
        self.position = start_pos
        self.epsilon_main *= max(self.epsilon_decay, self.epsilon_min)


    def choose_action(self, state: tuple):

        if random.random() < self.epsilon_main:
            return random.choice(self.actions)
        else:
            q_values = []

            for action in self.actions:
                key = (state, action)
                q = self.q_table.get(key, 0)
                q_values.append((q, action))

            max_q = max(q_values, key=lambda x : x[0])[0]
            best_action = [a for (q, a) in q_values if q == max_q]

            return random.choice(best_action)


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


    def move(self, action: str):
        dx = 0
        dy = 0
        x, y = self.position

        if action == "up":
            dy = -1
        elif action == "down":
            dy = 1
        elif action == "left":
            dx = -1
        elif action == "right":
            dx = 1

        x += dx
        y += dy
        self.position = (x, y)