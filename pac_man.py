import arcade

from src.maze import MazeLoader
from src.parser import Parser
from src.player import Player
from tests.maze_test import TestView


def main() -> None:
    parser = Parser("config.json")
    config = parser.load()
    maze = MazeLoader(config.levels[0]).load()
    player = Player(maze, config.lives, speed=4)

    window = arcade.Window(
        config.window_width,
        config.window_height,
        "PacMan Maze Test",
        update_rate=1 / config.fps,
    )
    window.show_view(TestView(maze, player))
    arcade.run()


if __name__ == "__main__":
    main()
