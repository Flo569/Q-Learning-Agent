from q_learning.tools.maze_file_reader import load_maze

# use this module to set variables

class Settings:

    # Logging
    ignored_head_vars = {
        "filename",
        "output_in_csv",
        "output_layout",
        "output_q_table",
        "output_detailed_log",
        "logging_steps",
        "ignored_head_vars",
        "log_vars",
        "rows",
        "columns",
        "start_pos",
        "goal_pos",
        "wall_pos",
        "bonus_pos",
        "layout",
        "log_maze"
    }
    log_vars = [
        "episode",
        "avg_steps",
        "avg_score",
        "avg_success",
        "avg_epsilon"
    ]

    filename: str = "Test"
    maze_directory: str = "11x11"         # directory used for maze-pool; relative to q_learning/mazes/
    log_maze: str = "maze_0.txt"            # file or maze you want to track (in directory)

    output_in_csv: bool = True              # if True -> .csv will be created

    logging_steps: int = 100

    # Training
    episodes: int = 10000
    max_steps_per_episode: int = 500

    # Agent-parameters – usual between 0-1
    alpha: float = 0.3
    gamma: float = 0.9
    epsilon_main: float = 1                 # start value
    epsilon_decay: float = 0.9          # multiplier
    epsilon_min: float = 0.1

    # Rewards
    step_reward: int = -1                   # reward used after each step
    goal_reward: int = 100                  # reward used after reaching the goal
    invalid_reward: int = -10               # reward used for invalid actions (wall)
    bonus_reward: int = 10                  # reward used after reaching a bonus item


    ### From here on, there are methods that are not important for configuration.
    ### They are not part of the settings.


    # Layout - used intern
    rows: int = 0
    columns: int = 0
    start_pos: tuple = (0, 0)               # (x, y)
    goal_pos: tuple = (0, 0)
    wall_pos: list[tuple] = []              # list of (x, y) -> [(x1, y1), (x2, y2), ...]
    bonus_pos: list[tuple] = []

    layout: list[list[int]] = []


    @classmethod
    def start(cls):
        from q_learning.core.agent import Agent
        agent = Agent()

        from q_learning.core.environment import Gridworld
        world = Gridworld(agent)

        world.train(cls.episodes)


    @classmethod
    def apply_special_squares_to_setting(cls):
        cls.rows = len(cls.layout)
        cls.columns = len(cls.layout[0])
        cls.wall_pos = []
        cls.bonus_pos = []
        for y in range(cls.rows):
            for x in range(cls.columns):
                if cls.layout[y][x] == 0: continue
                square_id = cls.layout[y][x]
                pos = (x, y)
                if square_id == 1:
                    cls.start_pos = pos
                elif square_id == 2:
                    cls.goal_pos = pos
                elif square_id == 3:
                    cls.wall_pos.append(pos)
                elif square_id == 4:
                    cls.bonus_pos.append(pos)


def implement_layout(filename: str):
    Settings.layout = load_maze(Settings.maze_directory, filename)      # load maze from file
    Settings.apply_special_squares_to_setting()                         # apply to vars - list -> vars