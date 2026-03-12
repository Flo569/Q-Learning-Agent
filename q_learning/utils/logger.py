import csv
import os
from q_learning.utils.settings import Settings

class Logger:

    last_episode: int = 0

    # vars to calculate the average value between run i - i2
    steps_sum: int = 0
    score_sum: int = 0
    success_sum: int = 0
    epsilon_sum: int = 0

    # lists to save the averages values between the mazes
    steps_avg: list = []
    score_avg: list = []
    success_avg: list = []
    epsilon_avg: list = []

    # lists to save multiple values over one run for detailed log
    states = []
    actions = []
    rewards = []
    new_states = []

    last_episodes: set = set()


    @classmethod
    def init_logger(cls):

        # logs-directory -> create directory if not existing
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


        ### filename

        # get filename from Settings or use "unnamed"
        if getattr(Settings, "filename", None) is None:  cls.name = "unnamed"
        else: cls.name = f"{Settings.filename}"

        # tests whether the name already exist and adds a unique number
        version: int = 0
        while os.path.exists(f"logs/data/training_{cls.name}.csv"):
            version += 1
            test_name = f"{cls.name}({version})"
            if not os.path.exists(f"logs/data/training_{test_name}.csv"):
                cls.name = f"{cls.name}({version})"
                break

        cls.filename = f"logs/data/training_{cls.name}.csv"


        ### layout
        cls.layout_name = f"logs/layout/layout_{cls.name}.csv"

        # adds the table-head for the layout.csv
        header = ["maze"]
        for name, value in Settings.__dict__.items():
            if name in ["rows", "columns", "start_pos", "goal_pos", "wall_pos", "bonus_pos", "layout"]:
                header.append(name)

        with open(cls.layout_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)


        ### q-table
        cls.q_table_name = f"logs/q_table/table_{cls.name}.csv"

        # adds the table-head for the q_table.csv
        with open(cls.q_table_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["episode", "q_table"])


        ### detailed-log

        cls.detail_name = f"logs/detailed_log/details_{cls.name}.csv"

        # adds the table-head for the log.csv
        with open(cls.detail_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["episode", "state", "action", "reward", "new_state"])


        ### head for settings -> logs all settings vars
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

        cls.create_log_head()


    @classmethod
    def create_log_head(cls):
        with open(cls.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(cls.header)                                             # write head
            writer.writerow(getattr(Settings, name) for name in cls.header)         # write values
            writer.writerow([])
            writer.writerow(Settings.log_vars)                                      # write head for log vars


    # logs properties of the maze
    @classmethod
    def log_layout(cls, filename: str):
        with open(cls.layout_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([filename, Settings.rows, Settings.columns, Settings.start_pos,
                             Settings.goal_pos, Settings.wall_pos, Settings.bonus_pos, Settings.layout])


    @classmethod
    def log_details(cls, filename: str, done: bool, episode: int,
                    state: tuple, action: str, reward: int, new_state: tuple,
                    q_table: dict):

        if not filename == Settings.log_maze: return                # only log right maze

        if (episode % Settings.logging_steps == 0                   # only if it's a step of logging_steps
                or episode == 1                                     # or the first run
                or episode == Settings.episodes + 1):               # or the final run

            # add values to list -> to store full run you need every step
            cls.states.append(state)
            cls.actions.append(action)
            cls.rewards.append(reward)
            cls.new_states.append(new_state)

            if not done: return         # if run completed, log data

            # log details in .csv
            with open(cls.detail_name, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([episode, cls.states, cls.actions, cls.rewards, cls.new_states])

            # clear lists for next run
            cls.states.clear()
            cls.actions.clear()
            cls.rewards.clear()
            cls.new_states.clear()

            # log q_table in .csv
            with open(cls.q_table_name, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([episode, q_table])


    @classmethod
    def log_episode(cls, episode: int, steps: int, score: int, success: bool, epsilon: float):

        # add values to vars
        cls.steps_sum += steps
        cls.score_sum += score
        cls.success_sum += success
        cls.epsilon_sum += epsilon

        if (episode % Settings.logging_steps == 0               # only if it's a step of logging_steps
                or episode == Settings.episodes + 1):           # or last run

            passed_episodes = episode - cls.last_episode

            # calculate averages
            avg_steps = cls.steps_sum / passed_episodes
            avg_score = cls.score_sum / passed_episodes
            avg_success = cls.success_sum / passed_episodes
            avg_epsilon = cls.epsilon_sum / passed_episodes

            index: int = episode // Settings.logging_steps

            if episode == Settings.episodes + 1:
                index += 1

            if len(cls.steps_avg) < index:
                cls.steps_avg.append([])
                cls.score_avg.append([])
                cls.success_avg.append([])
                cls.epsilon_avg.append([])

            # add the values to a list; like this:
            # [ [maze_0_avg, maze_1_avg, ... ]      0 - 100
            #   [maze_0_avg, maze_1_avg, ... ]      101 - 200
            #   [maze_0_avg, maze_1_avg, ... ]      201 - 300
            #   ...
            # ]
            index -= 1
            cls.steps_avg[index].append(avg_steps)
            cls.score_avg[index].append(avg_score)
            cls.success_avg[index].append(avg_success)
            cls.epsilon_avg[index].append(avg_epsilon)

            cls.last_episodes.add((cls.last_episode, episode))
            cls.last_episode = episode

            # reset var_sum for next iteration
            cls.steps_sum = 0
            cls.score_sum = 0
            cls.success_sum = 0
            cls.epsilon_sum = 0


    # logs average values among the mazes and episodes
    @classmethod
    def final_log(cls):
        with open(cls.filename, mode='a', newline='') as file:
            writer = csv.writer(file)

            sorted_files = sorted(cls.last_episodes)

            for i, obj in enumerate(sorted_files):

                if i >= len(cls.steps_avg): return          # protection of exceptions

                avg_steps = sum(cls.steps_avg[i]) / len(cls.steps_avg[i])
                avg_score = sum(cls.score_avg[i]) / len(cls.score_avg[i])
                avg_success = sum(cls.success_avg[i]) / len(cls.success_avg[i])
                avg_epsilon = sum(cls.epsilon_avg[i]) / len(cls.epsilon_avg[i])
                if not avg_epsilon == 0:                                        # final run without epsilon
                    avg_epsilon = max(avg_epsilon, Settings.epsilon_min)        # real epsilon is changed by epsilon_min

                writer.writerow([f"{obj[0]}-{obj[1]}", avg_steps, avg_score, avg_success, avg_epsilon])


    @classmethod
    def reset(cls):
        # reset between runs
        cls.last_episode = 0
        cls.steps_sum = 0
        cls.score_sum = 0
        cls.success_sum = 0
        cls.epsilon_sum = 0
        cls.states.clear()
        cls.actions.clear()
        cls.new_states.clear()
        cls.rewards.clear()
