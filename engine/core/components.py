from enum import Enum

from .ecs import Component
from .primitives import Integer, String
from .primitives import Position, Rotation

class ComponentNum(Enum):
    Cell = 1
    Transform = 2
    Identity = 3
    NumGrid = 9
    Custom = 10

class Cell(Component):
    row = Integer()
    col = Integer()
    val = Integer()

class Transform(Component):
    pos = Position()
    rot = Rotation()

class Identity(Component):
    name = String()

class NumGrid(Component):
    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        self.eids = []

    def create(self, width, height):
        self.width = width
        self.height = height
        self.eids = [0] * height * width

    def set(self, row, col, eid):
        offset = self.width * row + col
        self.eids[offset] = eid

    def get(self, row, col):
        offset = self.width * row + col
        return self.eids[offset]

