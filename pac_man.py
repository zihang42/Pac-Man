import arcade

from src.parser import Parser
from tests.maze_test import TestView


def main() -> None:
    parser = Parser("config.json")
    config = parser.load()

    window = arcade.Window(
        config.window_width,
        config.window_height,
        "PacMan Maze Test",
        update_rate=1 / config.fps,
    )
    window.show_view(
        TestView(
            config,
            level_index=0,
            player_speed=4,
            ghost_speed=3,
            is_cheat_mode=True,
        )
    )
    arcade.run()


if __name__ == "__main__":
    main()
