from src.parser import Parser
from visualizer import Pacman


def main() -> None:
    print("Hello from pac-man!")
    parser = Parser("config.json")
    data = parser.load()
    print(data)
    pacman_visu = Pacman()
    pacman_visu.start()


if __name__ == "__main__":
    main()
