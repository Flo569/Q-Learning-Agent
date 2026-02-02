import settings
from settings import Settings

def main():
    Settings.create_environment()
    Settings.create_agent()
    settings.implement_layout()
    Settings.print_layout()
    Settings.world.train(Settings.episodes)

if __name__ == "__main__":
    main()