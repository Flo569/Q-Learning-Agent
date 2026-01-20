import random

import agent

class Gridworld:

    def __init__(self):

        self.columns = 10
        self.rows = 10

        self.target = (9, 9)

        self.my_agent = agent.Agent((self.columns, self.rows))

        self.world = []

        for column in range(self.columns):
            for row in range(self.rows):
                self.world.append((column, row))


    def reset(self):

        self.target = (9, 9)
        self.my_agent.score = 0
        self.set_agent()


    def set_agent(self):

        x = random.randint(0, self.columns - 1)
        y = random.randint(0, self.rows - 1)

        self.my_agent.position = (x, y)


    def train(self, episodes):
        for i in range(episodes):
            self.reset()
            self.start_run()
            self.my_agent.epsilon *= 0.995
            self.my_agent.epsilon = max(self.my_agent.epsilon, 0.01)

        for key, value in self.my_agent.q_table.items():
            print(key, "->", value)

    def start_run(self):

        state = self.my_agent.position

        while True:

            action = self.my_agent.choose_action(state)
            self.my_agent.move(action)
            new_state = self.my_agent.position

            if new_state == self.target:
                reward = 100
                done = True
            elif new_state == state:
                reward = -10
                done = False
            else:
                reward = -1
                done = False

            self.my_agent.learn(state, action, reward, new_state)
            state = new_state

            if done:
                print('Target reached with a score of: ', self.my_agent.score + 100)
                break