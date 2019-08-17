from enum import Enum

from .data import Model
from .primitives import Integer

class EventNum(Enum):
    Default = 0
    App = 0
    World = 0
    Key = 1

class KeyNum(Enum):
    Unknown = 0
    Up = 1
    Down = 2
    Left = 4
    Right = 8
    Escape = 100

class Event(Model):
    @property
    def num(self):
        return EventNum.Default

class AppEvent(Event):
    pass

class WorldOpened(Event):
    pass

class WorldClosing(Event):
    pass

class KeyEvent(Event):
    @property
    def num(self):
        return EventNum.Key

    key_num = Integer() # KeyNum
    memo = Integer() # Memo

class KeyPressed(KeyEvent):
    pass

