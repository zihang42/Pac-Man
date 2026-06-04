from enum import Enum

from src.maze import Maze
from src.utils import DIRECTION, Position


class GhostState(Enum):
    CHASE = "chase"
    FRIGHTEN = "frighten"
    EATEN = "eaten"


class Ghost:
    def __init__(self, maze: Maze, pos: Position, speed: int) -> None:
        self.maze = maze
        self.home = pos
        self.pos = pos
        self.speed = speed
        self.state = GhostState.CHASE
        self.state_time = 0.0
        self.direction = DIRECTION.RIGHT
        self.target = None
        self.is_alive = True
        self.row = float(self.pos.x)
        self.col = float(self.pos.y)

    def move(self, direction: DIRECTION) -> None:
        """Move one cell in the given direction if the path is open."""
        self.direction = direction
        if self.state == GhostState.EATEN:
            return
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

    def get_eaten(self) -> None:
        """Ghost is eaten by the player"""
        if not self.is_alive:
            return
        self.state = GhostState.EATEN
        self.is_alive = False

    def get_frightened(self) -> None:
        """Ghost is frightened by the player"""
        if not self.is_alive:
            return
        self.state = GhostState.FRIGHTEN

    def respawn(self) -> None:
        """Ghost respawns back to the initial state"""
        self.pos = self.home
        self.row = float(self.pos.x)
        self.col = float(self.pos.y)
        self.direction = DIRECTION.RIGHT
        self.target = None
        self.state = GhostState.CHASE
        self.is_alive = True

    def on_update(self, delta_time: float) -> None:
        pass
