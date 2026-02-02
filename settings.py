
class Settings:

    # Training
    episodes: int = 1000
    max_steps_per_episode: int = 250

    # Agent
    alpha: float = 0.1
    gamma: float = 0.9
    epsilon_main: float = 0.2
    epsilon_decay: float = 0.99

    # Rewards
    step_reward: int = -1
    goal_reward: int = 100
    invalid_reward: int = -10
    bonus_reward: int = 10

    # Layout
    rows: int = 10
    columns: int = 10
    start_pos: tuple[int, int] = (0, 0)
    goal_pos: tuple[int, int] = (9, 9)
    wall_pos: list[tuple[int, int]] = [(5, 5), (6, 5)]
    bonus_pos: list[tuple[int, int]] = [(7, 7), (1, 2)]

    # Custom layout for more complex designs.
    # Overrides the layout settings!
    # Rows and columns must be all the same size!

    # 0 = empty square
    # 1 = start (only one)
    # 2 = goal  (only one)
    # 3 = wall  (auto built a border)
    # 4 = bonus item

    # Example
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

    # Use None to apply the layout settings -> ... = None
    layout: list[list[int]] = example_layout()


    ### From here on, there are methods that are not important for configuration.
    ### They are not part of the settings.

    @classmethod
    def create_agent(cls):
        from agent import Agent
        cls.agent: Agent = Agent(cls.alpha, cls.gamma, cls.epsilon_main, cls.epsilon_decay)

    @classmethod
    def create_environment(cls):
        from environment import Gridworld
        cls.world: Gridworld = Gridworld(cls.rows, cls.columns, cls.start_pos, cls.goal_pos, cls.wall_pos, cls.bonus_pos)

    agent = None
    world = None

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
                elif cls.wall_pos.__contains__(pos):
                    cls.layout[y][x] = 3
                elif cls.bonus_pos.__contains__(pos):
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
    Settings.apply_layout()
    Settings.default_layout()
    Settings.apply_special_squares_to_layout()