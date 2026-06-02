from src.maze import MazeLoader
from src.parser import Parser
from visualizer import Window


def main() -> None:
    print("Hello from pac-man!")
    parser = Parser("config.json")
    config = parser.load()
    maze = MazeLoader(config.levels[1]).load()
    print(maze)
    pacman_visu = Window(config.window_width, config.window_height, config.fps)
    pacman_visu.start()


if __name__ == "__main__":
    main()
