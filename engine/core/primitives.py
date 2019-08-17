from engine.core.data import Primitive

class Integer(Primitive):
    def __init__(self, *args, **kwargs):
        Primitive.__init__(self, 'i', 0, *args, **kwargs)
        self.min = -0x800000000000000
        self.max = +0x7FFFFFFFFFFFFFF

    def convert(self, value):
        ret_value = int(value)
        if ret_value < self.min: raise PrimitiveError('UNDERFLOW', ret_value, f"< {self.min}")
        if ret_value > self.max: raise PrimitiveError('OVERFLOW', ret_value, f"> {self.max}")
        return ret_value

class Float(Primitive):
    def __init__(self, *args, **kwargs):
        Primitive.__init__(self, 'f', 0.0, *args, **kwargs)

    def convert(self, value):
        return float(value)
    
class String(Primitive):
    def __init__(self, *args, **kwargs):
        Primitive.__init__(self, 's', "", *args, **kwargs)

    def convert(self, value):
        return str(value)

class Position(Primitive):
    def __init__(self, *args, **kwargs):
        Primitive.__init__(self, 'p', (0, 0, 0), *args, **kwargs)

class Rotation(Primitive):
    def __init__(self, *args, **kwargs):
        Primitive.__init__(self, 'd', 0, *args, **kwargs) # 0: x+

