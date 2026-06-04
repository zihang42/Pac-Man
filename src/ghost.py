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
        self.pos = pos
        self.speed = speed
        self.state = GhostState.CHASE
        self.state_time = 0.0
        self.direction = DIRECTION.RIGHT
        self.target = None
        self.is_alive = True
        self.row = float(self.pos.x)
        self.col = float(self.pos.y)
