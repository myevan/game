from enum import Enum

from .ecs import Component
from .primitives import Integer, String
from .primitives import Position, Rotation

class ComponentNum(Enum):
    Cell = 1

class Cell(Component):
    row = Integer()
    col = Integer()
    val = Integer()

class Transform(Component):
    pos = Position()
    rot = Rotation()

class Identity(Component):
    name = String()

