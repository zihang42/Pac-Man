from src.logger import logger
from src.maze import Maze
from src.utils import DIRECTION, Position


class Player:
    """Player state and one-cell movement rules."""

    def __init__(self, maze: Maze, lives: int, speed: int) -> None:
        self.maze = maze
        self.lives = lives
        self.speed = speed
        self.score = 0
        self.is_alive = True
        self.pos = Position(maze.height // 2, maze.width // 2)
        self.direction = DIRECTION.RIGHT

    def move(self, direction: DIRECTION) -> None:
        """Move one cell in the given direction if the path is open."""
        self.direction = direction
        if not self.maze.can_move(self.pos, direction):
            return

        if direction == DIRECTION.UP:
            self.pos = Position(self.pos.x - 1, self.pos.y)
        elif direction == DIRECTION.DOWN:
            self.pos = Position(self.pos.x + 1, self.pos.y)
        elif direction == DIRECTION.LEFT:
            self.pos = Position(self.pos.x, self.pos.y - 1)
        elif direction == DIRECTION.RIGHT:
            self.pos = Position(self.pos.x, self.pos.y + 1)

    def lose_life(self) -> None:
        """Decrease player lives by one."""
        self.lives = max(0, self.lives - 1)
        self.is_alive = self.lives > 0
        logger.info(f"Ah oh, you died... {self.lives} remaining")

    def respawn(self) -> None:
        """Respawn the player at the center of the maze."""
        self.pos = Position(self.maze.height // 2, self.maze.width // 2)
        self.direction = DIRECTION.RIGHT
        self.is_alive = True
        logger.info(f"Player is respawned at {self.pos}")

    def add_score(self, point: int) -> None:
        """Add score points."""
        self.score += point
