from src.maze import MazeLoader
from src.parser import Parser

from visualizer import Window


def main() -> None:
    print("Hello from pac-man!")
    parser = Parser("config.json")
    config = parser.load()
    maze = MazeLoader(config.levels[0]).load()
    print_maze(maze)
    pacman_visu = Window(config.window_width,
                         config.window_height,
                         config.fps)
    pacman_visu.start()


def print_maze(maze) -> None:
    """
    An example to draw the 42 pattern,
    the maze libaray doesn't indicate the 42 cell,
    but you can use grid[i][j].is_42_pattern, it
    doesn't 100% accurate but it will work most
    of the time
    """
    grid = maze.cells
    height, width = maze.height, maze.width
    print(width, height)
    print("+" + "---+" * width)
    for i in range(height):
        row = "|"
        for j in range(width):
            if grid[i][j].is_42_pattern:
                cell = "###"
            else:
                cell = "   "

            if grid[i][j].east_wall:
                row += cell + "|"
            else:
                row += cell + " "
        print(row)
        bottom = "+"
        for j in range(width):
            if grid[i][j].south_wall:
                bottom += "---+"
            else:
                bottom += "   +"
        print(bottom)


if __name__ == "__main__":
    main()
