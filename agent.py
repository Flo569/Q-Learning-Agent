import random


class Agent:

    def __init__(self, world_border):

        self.columns, self.rows = world_border
        self.position = (0, 0)
        self.score = 0

        self.q_table = {}
        self.actions = ["up", "down", "left", "right"]

        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 1

        for x in range(self.columns):
            for y in range(self.rows):
                for action in self.actions:
                    self.q_table[((x, y), action)] = 0


    def choose_action(self, state):

        if random.random() < self.epsilon:
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


    def learn(self, state, action, reward, new_state):

        key = (state, action)

        current_q = self.q_table.get(key, 0)

        max_future_q = max([self.q_table.get((new_state, a), 0) for a in self.actions])

        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)

        self.q_table[key] = new_q


    def move(self, direction):

        dx = 0
        dy = 0
        x, y = self.position

        if direction == "up":
            dx = 0
            dy = -1
        elif direction == "down":
            dx = 0
            dy = 1
        elif direction == "left":
            dx = -1
            dy = 0
        elif direction == "right":
            dx = 1
            dy = 0

        if not x + dx < 0 and not x + dx >= self.columns:
            x += dx

        if not y + dy < 0 and not y + dy >= self.rows:
            y += dy

        self.score -= 1
        self.position = (x, y)