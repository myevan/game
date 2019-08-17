from ..core.data import Model
from ..core.primitives import Integer, Float, String

class Base(Model):
    pass

class float_t(Float):
    def __init__(self, *args, **kwargs):
        Float.__init__(self, *args, **kwargs)
        self.prefix = 'f32'

class uint_t(Integer):
    def __init__(self, *args, **kwargs):
        Integer.__init__(self, *args, **kwargs)
        self.min = 0
        self.max = 0xFFFFFFFF

class int_t(Integer):
    def __init__(self, *args, **kwargs):
        Integer.__init__(self, *args, **kwargs)
        self.min = -0x80000000
        self.max = +0x7FFFFFFF

class char_t(int_t):
    def __init__(self, *args, **kwargs):
        int_t.__init__(self, *args, **kwargs)
        self.prefix = 'sz'
        self.min = 0
        self.max = 0x7F

    def convert(self, value):
        ret_value = str(value)
        enc_value = ret_value.encode('utf-8')
        enc_len = len(enc_value)
        enc_max = self.count - 1
        if enc_len > enc_max: 
            enc_clamp = enc_value[:enc_max]
            clamp = enc_clamp.decode('utf-8', 'ignore')
            over = ret_value[len(clamp):]
            raise PrimitiveError('OVERFLOW', f"{clamp}({over})", f"len({enc_len + 1}) > cap({self.count})")

        return ret_value

class int8_t(int_t):
    def __init__(self, *args, **kwargs):
        int_t.__init__(self, *args, **kwargs)
        self.prefix = 'i8'
        self.min = -0x80
        self.max = +0x7F

    def convert(self, value):
        return int_t.convert(self, value)

class int16_t(int_t):
    def __init__(self, *args, **kwargs):
        int_t.__init__(self, *args, **kwargs)
        self.prefix='i16'
        self.min = -0x8000
        self.max = +0x7FFF

class int32_t(int_t):
    def __init__(self, *args, **kwargs):
        int_t.__init__(self, *args, **kwargs)
        self.prefix='i32'
        self.min = -0x80000000
        self.max = +0x7FFFFFFF

class int64_t(int_t):
    def __init__(self, *args, **kwargs):
        int_t.__init__(self, *args, **kwargs)
        self.prefix='i64'
        self.min = -0x8000000000000000
        self.max = +0x7FFFFFFFFFFFFFFF

class uint8_t(uint_t):
    def __init__(self, *args, **kwargs):
        uint_t.__init__(self, *args, **kwargs)
        self.prefix = 'u8'
        self.min = 0
        self.max = 0xFF

class uint16_t(uint_t):
    def __init__(self, *args, **kwargs):
        uint_t.__init__(self, *args, **kwargs)
        self.prefix = 'u16'
        self.min = 0
        self.max = 0xFFFF

class uint32_t(uint_t):
    def __init__(self, *args, **kwargs):
        uint_t.__init__(self, *args, **kwargs)
        self.prefix = 'u32'
        self.min = 0
        self.max = 0xFFFFFFFF

class uint64_t(uint_t):
    def __init__(self, *args, **kwargs):
        uint_t.__init__(self, *args, **kwargs)
        self.prefix = 'u64'
        self.min = 0
        self.max = 0xFFFFFFFFFFFFFFFF

class time_t(uint32_t):
    pass
