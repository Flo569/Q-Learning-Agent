import settings
from settings import Settings
import gridworld

def main():
    settings.implement_layout()
    Settings.print_layout()
    my_world = gridworld.Gridworld()
    my_world.train(100)

if __name__ == "__main__":
    main()