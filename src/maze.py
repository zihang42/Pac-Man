import random
from dataclasses import dataclass

from mazegenerator.mazegenerator import MazeGenerator

from src.parser import LevelConfig


@dataclass(frozen=True)
class Cell:
    north_wall: bool
    east_wall: bool
    south_wall: bool
    west_wall: bool


@dataclass(frozen=True)
class Maze:
    width: int
    height: int
    cells: list[list[Cell]]


class MazeLoader:
    """
    load the level config and convert the maze
    """

    def __init__(self, level: LevelConfig) -> None:
        self.level = level

    def load(self) -> Maze:
        seed = (
            random.randint(1, 999)
            if self.level.seed is None
            else self.level.seed
        )
        generator = MazeGenerator(
            (self.level.width, self.level.height),
            False,
            (0, 0),
            (self.level.width - 1, self.level.height - 1),
            seed,
        )
        self._maze = generator.maze
        self._cells = []
        for row in self._maze:
            cells = []
            for col in row:
                cells.append(
                    Cell(
                        north_wall=col & 1 != 0,
                        east_wall=col & 2 != 0,
                        south_wall=col & 4 != 0,
                        west_wall=col & 8 != 0,
                    )
                )
            self._cells.append(cells)
        return Maze(self.level.width, self.level.height, self._cells)
