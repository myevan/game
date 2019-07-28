from engine.protocol import *

class User(Base):
    id = int32_t(pk=True)
    name = char_t(32)