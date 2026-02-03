from settings import Settings

def main():
    Settings.print_layout()
    Settings.create_environment()
    Settings.create_agent()
    Settings.world.train(Settings.episodes)

if __name__ == "__main__":
    main()