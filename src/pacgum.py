from dataclasses import dataclass

from src.utils import Position


@dataclass
class Pacgum:
    pos: Position
    points: int


@dataclass
class SuperPacgum(Pacgum):
    duration_of_frighten: float
