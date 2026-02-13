import csv
import os
from q_learning.utils.settings import Settings

class Logger:

    last_episode: int = 0

    steps_sum: int = 0
    score_sum: int = 0
    success_sum: int = 0
    epsilon_sum: int = 0

    states = []
    actions = []
    rewards = []
    new_states = []

    @classmethod
    def init_logger(cls):
        # logs-directory
        if not os.path.exists("./logs"):
            os.makedirs("./logs")
        if not os.path.exists("./logs/data"):
            os.makedirs("./logs/data")
        if not os.path.exists("./logs/layout"):
            os.makedirs("./logs/layout")
        if not os.path.exists("./logs/q_table"):
            os.makedirs("./logs/q_table")
        if not os.path.exists("./logs/detailed_log"):
            os.makedirs("./logs/detailed_log")

        # filename
        if getattr(Settings, "filename", None) is None:
            cls.name = "unnamed"
        else:
            cls.name = f"{Settings.filename}"
        version: int = 0
        while os.path.exists(f"logs/data/training_{cls.name}.csv"):
            version += 1
            test_name = f"{cls.name}({version})"
            if not os.path.exists(f"logs/data/training_{test_name}.csv"):
                cls.name = f"{cls.name}({version})"

        cls.filename = f"logs/data/training_{cls.name}.csv"

        # layout
        if Settings.output_layout:
            cls.layout_name = f"logs/layout/layout_{cls.name}.csv"

            header = []

            for name, value in Settings.__dict__.items():
                if name in ["rows", "columns", "size", "start_pos", "goal_pos", "wall_pos", "bonus_pos", "layout"]:
                    header.append(name)

            with open(cls.layout_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerow(getattr(Settings, name) for name in header)

        # q-table
        cls.q_table_name = f"logs/q_table/table_{cls.name}.csv"

        if Settings.output_q_table:
            with open(cls.q_table_name, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["episode", "q_table"])


        # detailed-log
        cls.detail_name = f"logs/detailed_log/details_{cls.name}.csv"

        if Settings.output_detailed_log:
            with open(cls.detail_name, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["episode", "state", "action", "reward", "new_state"])


        # head for settings
        ALLOWED_TYPES = (int, float, str, bool, tuple, list)

        cls.header = []
        for name, value in Settings.__dict__.items():

            if name.startswith("__"):
                continue
            if name in Settings.ignored_head_vars:
                continue
            if not isinstance(value, ALLOWED_TYPES):
                continue

            cls.header.append(name)


    @classmethod
    def create_log_head(cls):
        with open(cls.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(cls.header)
            writer.writerow(getattr(Settings, name) for name in cls.header)
            writer.writerow([])
            writer.writerow(Settings.log_vars)


    @classmethod
    def log_details(cls, done: bool, episode: int, state: tuple, action: str, reward: int, new_state: tuple):
        if episode % Settings.logging_steps == 0 or episode == 1 or episode == Settings.episodes + 1:
            cls.states.append(state)
            cls.actions.append(action)
            cls.rewards.append(reward)
            cls.new_states.append(new_state)

            if done:
                with open(cls.detail_name, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([episode, cls.states, cls.actions, cls.rewards, cls.new_states])

                cls.states.clear()
                cls.actions.clear()
                cls.rewards.clear()
                cls.new_states.clear()


    @classmethod
    def log_episode(cls, episode: int, steps: int, score: int, success: bool, epsilon: float, q_table: dict):
        cls.steps_sum += steps
        cls.score_sum += score
        cls.success_sum += success
        cls.epsilon_sum += epsilon

        if episode % Settings.logging_steps == 0 or episode == Settings.episodes + 1:
            passed_episodes = episode - cls.last_episode

            avg_steps = cls.steps_sum / passed_episodes
            avg_score = cls.score_sum / passed_episodes
            avg_success = cls.success_sum / passed_episodes
            avg_epsilon = cls.epsilon_sum / passed_episodes

            with open(cls.filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([f"{cls.last_episode}–{episode}", avg_steps, avg_score, avg_success, avg_epsilon])

            cls.last_episode = episode
            cls.steps_sum = 0
            cls.score_sum = 0
            cls.success_sum = 0
            cls.epsilon_sum = 0

            if Settings.output_q_table:
                with open(cls.q_table_name, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([episode, q_table])