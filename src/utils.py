from dataclasses import dataclass
from enum import Enum


class DIRECTION(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


@dataclass
class Position:
    x: int
    y: int
