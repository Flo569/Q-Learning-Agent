
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
    }
    log_vars = [
        "episode",
        "avg_steps",
        "avg_score",
        "avg_success",
        "avg_epsilon"
    ]

    filename: str = "Random"
    output_in_csv: bool = True
    output_layout: bool = True
    output_detailed_log: bool = True
    output_q_table: bool = True

    logging_steps: int = 100

    # Training
    episodes: int = 1000
    max_steps_per_episode: int = 250

    # Agent-parameters
    alpha: float = 0.3
    gamma: float = 0.8
    epsilon_main: float = 1
    epsilon_decay: float = 0.995
    epsilon_min: float = 0.0

    # Rewards
    step_reward: int = -1
    goal_reward: int = 100
    invalid_reward: int = -10
    bonus_reward: int = 10

    # Layout
    rows: int = 10
    columns: int = 10
    size: str = f"{rows}x{columns}"
    start_pos: tuple = (0, 0)
    goal_pos: tuple = (9, 9)
    wall_pos: list[tuple] = []
    bonus_pos: list[tuple] = []

    # Custom layout
    # Overrides the layout settings!
    @staticmethod
    def example_layout():
        return [
            [1, 3, 0, 0, 0, 0, 0, 3, 0, 0],
            [0, 3, 0, 3, 3, 3, 0, 3, 0, 0],
            [0, 3, 0, 3, 0, 0, 0, 3, 0, 0],
            [0, 3, 0, 3, 0, 3, 3, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 3, 3, 3, 0, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 3, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 3, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 3, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 3, 0, 2, 0]
        ]
    # 0 = empty square
    # 1 = start (only one)
    # 2 = goal  (only one)
    # 3 = wall  (auto built a border around the grid)
    # 4 = bonus item

    # Use None to apply the layout settings -> ... = None
    layout: list[list[int]] = None


    ### From here on, there are methods that are not important for configuration.
    ### They are not part of the settings.


    @classmethod
    def start(cls):
        from q_learning.core.agent import Agent
        agent = Agent(cls.alpha, cls.gamma, cls.epsilon_main, cls.epsilon_decay, cls.epsilon_min)

        from q_learning.core.environment import Gridworld
        world = Gridworld(agent, cls.rows, cls.columns, cls.start_pos, cls.goal_pos, cls.wall_pos, cls.bonus_pos)

        world.train(cls.episodes)


    # Layout methods
    @classmethod
    def print_layout(cls):
        for row in cls.layout:
            print(row)


    @classmethod
    def default_layout(cls):
        cls.layout = [[0 for _ in range(cls.columns)] for _ in range(cls.rows)]


    @classmethod
    def apply_special_squares_to_layout(cls):
        for y in range(cls.rows):
            for x in range(cls.columns):
                pos = (x, y)
                if pos == cls.start_pos:
                    cls.layout[y][x] = 1
                elif pos == cls.goal_pos:
                    cls.layout[y][x] = 2
                elif pos in cls.wall_pos:
                    cls.layout[y][x] = 3
                elif pos in cls.bonus_pos:
                    cls.layout[y][x] = 4


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


    @classmethod
    def apply_layout(cls):
        if cls.layout is None: return
        cls.apply_special_squares_to_setting()


def implement_layout():
    Settings.apply_layout()                         # layout -> settings; if layout = None -> ignored
    Settings.default_layout()                       # empty grid
    Settings.apply_special_squares_to_layout()      # settings -> layout

implement_layout()