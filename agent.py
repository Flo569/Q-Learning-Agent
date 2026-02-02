import random
from settings import Settings

class Agent:

    def __init__(self, alpha: float, gamma: float, epsilon_main: float, epsilon_decay: float):

        self.position = (0, 0)
        self.score = 0

        self.q_table = {}
        self.actions = ["up", "down", "left", "right"]

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_main = epsilon_main
        self.epsilon_decay = epsilon_decay

        for x in range(Settings.world.columns):
            for y in range(Settings.world.rows):
                for action in self.actions:
                    self.q_table[((x, y), action)] = 0


    def reset(self, start_pos: tuple[int, int]):
        self.score = 0
        self.position = start_pos
        self.epsilon_main *= self.epsilon_decay


    def choose_action(self, state: tuple[int, int]):

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


    def learn(self, state: tuple[int, int], action: str, reward: int, new_state: tuple[int, int]):
        self.score += reward
        key = (state, action)
        current_q = self.q_table.get(key, 0)
        max_future_q = max([self.q_table.get((new_state, a), 0) for a in self.actions])
        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
        self.q_table[key] = new_q


    def move(self, action: str):
        dx = 0
        dy = 0
        x, y = self.position

        if action == "up":
            dx = 0
            dy = -1
        elif action == "down":
            dx = 0
            dy = 1
        elif action == "left":
            dx = -1
            dy = 0
        elif action == "right":
            dx = 1
            dy = 0

        x += dx
        y += dy
        self.position = (x, y)