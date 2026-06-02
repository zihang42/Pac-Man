from src.logger import logger
from src.maze import Maze
from src.utils import DIRECTION, Position


class Player:
    def __init__(self, maze: Maze, lives: int) -> None:
        self.pos = Position(maze.height // 2, maze.width // 2)
        self.lives = lives
        self.score = 0
        self.maze = maze

    def move(self, direction: DIRECTION) -> None:
        x = self.pos.x
        y = self.pos.y
        if not self.maze.can_move(self.pos, direction):
            return
        if direction == DIRECTION.UP:
            self.pos = Position(x - 1, y)
        elif direction == DIRECTION.DOWN:
            self.pos = Position(x + 1, y)
        elif direction == DIRECTION.RIGHT:
            self.pos = Position(x, y + 1)
        elif direction == DIRECTION.LEFT:
            self.pos = Position(x, y - 1)

    def lose_life(self) -> None:
        self.lives = max(0, self.lives - 1)
        logger.info(f"Ah oh, you died... {self.lives} remaining")

    def respawn(self) -> None:
        self.pos = Position(self.maze.height // 2, self.maze.width // 2)

    def add_score(self, point: int) -> None:
        self.score += point
