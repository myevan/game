from ..core import data as db

class Base(db.Model):
    pass

class float_t(db.Float):
    def __init__(self, *args, **kwargs):
        db.Float.__init__(self, *args, **kwargs)
        self.prefix = 'f32'

class uint_t(db.Integer):
    def __init__(self, *args, **kwargs):
        db.Integer.__init__(self, *args, **kwargs)

class int_t(db.Integer):
    def __init__(self, *args, **kwargs):
        db.Integer.__init__(self, *args, **kwargs)

class char_t(int_t):
    def __init__(self, *args, **kwargs):
        int_t.__init__(self, *args, **kwargs)
        self.prefix = 'sz'
        self.min = 0
        self.max = 0x7F

    def convert(self, value):
        ret_value = str(value)
        enc_value = ret_value.encode('utf-8')
        limit = self.count - 1
        if len(enc_value) > limit: 
            clamp = enc_value[:limit].decode('utf-8', 'ignore')
            over = ret_value[len(clamp):]
            raise db.PrimitiveError('OVERFLOW', f"{clamp}({over})", limit)

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
        self.max = 0xFF

class uint16_t(uint_t):
    def __init__(self, *args, **kwargs):
        uint_t.__init__(self, *args, **kwargs)
        self.prefix = 'u16'
        self.max = 0xFFFF

class uint32_t(uint_t):
    def __init__(self, *args, **kwargs):
        uint_t.__init__(self, *args, **kwargs)
        self.prefix = 'u32'
        self.max = 0xFFFFFFFF

class uint64_t(uint_t):
    def __init__(self, *args, **kwargs):
        uint_t.__init__(self, *args, **kwargs)
        self.prefix = 'u64'
        self.max = 0xFFFFFFFFFFFFFFFF

class time_t(uint32_t):
    pass
