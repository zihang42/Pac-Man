from src.logger import logger
from src.maze import Maze
from src.utils import DIRECTION, Position

OFFSETS = {
    DIRECTION.UP: (-1, 0),
    DIRECTION.DOWN: (1, 0),
    DIRECTION.LEFT: (0, -1),
    DIRECTION.RIGHT: (0, 1),
}


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
        self.request_direction = DIRECTION.RIGHT
        self.target: Position | None = None
        self.row = float(self.pos.x)
        self.col = float(self.pos.y)

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
        self.row = float(self.pos.x)
        self.col = float(self.pos.y)

    def lose_life(self) -> None:
        """Decrease player lives by one."""
        self.lives = max(0, self.lives - 1)
        self.is_alive = self.lives > 0
        logger.info(f"Ah oh, you died... {self.lives} remaining")

    def respawn(self) -> None:
        """Respawn the player at the center of the maze."""
        self.pos = Position(self.maze.height // 2, self.maze.width // 2)
        self.direction = DIRECTION.RIGHT
        self.request_direction = DIRECTION.RIGHT
        self.target = None
        self.row = float(self.pos.x)
        self.col = float(self.pos.y)
        self.is_alive = True
        logger.info(f"Player is respawned at {self.pos}")

    def add_score(self, point: int) -> None:
        """Add score points."""
        self.score += point

    def set_direction(self, direction: DIRECTION) -> None:
        self.request_direction = direction

    def on_update(self, delta_time: float) -> None:
        """Move the player according to elapsed time."""
        if not self.is_alive:
            return
        distance = max(0, delta_time) * max(1, self.speed)
        while distance > 0:
            if self.target is None:
                if self.maze.can_move(self.pos, self.request_direction):
                    self.direction = self.request_direction
                if self.maze.can_move(self.pos, self.direction):
                    self.target = Position(
                        self.pos.x + OFFSETS[self.direction][0],
                        self.pos.y + OFFSETS[self.direction][1],
                    )
                else:
                    break
            distance = self._move_to_target(distance)

    def _move_to_target(self, distance: float) -> float:
        """Move toward target and return leftover distance."""
        if not self.target:
            return 0.0
        distance_x = self.target.x - self.row
        distance_y = self.target.y - self.col
        target_distance = abs(distance_x) + abs(distance_y)
        if target_distance <= distance:
            distance -= target_distance
            self.pos = self.target
            self.row = float(self.pos.x)
            self.col = float(self.pos.y)
            self.target = None
            return distance
        ratio = distance / target_distance
        self.row += distance_x * ratio
        self.col += distance_y * ratio
        return 0.0
