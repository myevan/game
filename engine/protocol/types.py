from ..core import data as db

class Base(db.Model):
    pass

class float_t(db.Float):
    def __init__(self, *args, **kwargs):
        db.Float.__init__(self, *args, **kwargs)
        self.prefix = 'f32'

class uint_t(db.Integer):
    def __init__(self, prefix, max, *args, **kwargs):
        db.Integer.__init__(self, 0, max, **kwargs)
        self.prefix = prefix

class int_t(db.Integer):
    def __init__(self, prefix, min, max, *args, **kwargs):
        db.Integer.__init__(self, min, max, **kwargs)
        self.prefix = prefix

class char_t(int_t):
    def __init__(self, *args, **kwargs):
        int_t.__init__(self, 'sz', 0, 0x7F, **kwargs)

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
        int_t.__init__(self, 'i8', -0x80, 0x7F, *args, **kwargs)

    def convert(self, value):
        return int_t.convert(value)

class int16_t(int_t):
    def __init__(self, *args, **kwargs):
        int_t.__init__(self, 'i16', -0x8000, 0x7FFF, *args, **kwargs)

class int32_t(int_t):
    def __init__(self, *args, **kwargs):
        int_t.__init__(self, 'i32', -0x80000000, 0x7FFFFFFF, *args, **kwargs)

class int64_t(int_t):
    def __init__(self, *args, **kwargs):
        int_t.__init__(self, 'i64', -0x8000000000000000, 0x7FFFFFFFFFFFFFFF, *args, **kwargs)

class uint8_t(uint_t):
    def __init__(self, *args, **kwargs):
        uint_t.__init__(self, 'u8', 0xFF, *args, **kwargs)

class uint16_t(uint_t):
    def __init__(self, *args, **kwargs):
        uint_t.__init__(self, 'u16', 0xFFFF, *args, **kwargs)

class uint32_t(uint_t):
    def __init__(self, *args, **kwargs):
        uint_t.__init__(self, 'u32', 0xFFFFFFFF, *args, **kwargs)

class uint64_t(uint_t):
    def __init__(self, *args, **kwargs):
        uint_t.__init__(self, 'u64', 0xFFFFFFFFFFFFFFFF, *args, **kwargs)

class time_t(uint32_t):
    pass
