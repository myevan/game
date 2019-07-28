from collections import OrderedDict

class Singleton:
    __inst = None

    @classmethod
    def get(cls):
        if cls.__inst is None:
            cls.__inst = cls()
        return cls.__inst

class KeySingleton:
    __insts = OrderedDict()

    @classmethod
    def get(cls, key):
        return cls.__insts.get(key)

    @classmethod
    def get_keys(cls):
        return cls.__insts.keys()

    @classmethod
    def get_items(cls):
        return cls.__insts.items()

    @classmethod
    def get_values(cls):
        return cls.__insts.values()

    @classmethod
    def spawn(cls, key, *args, **kwargs):
        inst = cls(key, *args, **kwargs)
        cls.__insts[key] = inst
        return inst

    def __init__(self, key, *args, **kwargs):
        self.__key = key

    @property
    def key(self):
        return self.__key

class Factory:
    def __init__(self):
        self.__key_create_insts = {}
        self.__def_create_inst = None

    def register(self, key, create_inst):
        self.__key_create_insts[key] = create_inst

    def register_default(self, create_inst):
        self.__def_create_inst = create_inst

    def create(self, key, *args, **kwargs):
        key_create_inst = self.__key_create_insts.get(key)
        if key_create_inst:
            return key_create_inst(*args, **kwargs)
        else:
            return self.__def_create_inst(*args, **kwargs)

class Cache:
    __insts = dict()

    @classmethod
    def get(cls, key):
        inst = cls.__insts.get(key)
        return inst if inst else cls.load(key)

    @classmethod
    def load(cls, key):
        inst = cls(key)
        cls.__insts[key] = inst
        return inst

    def __init__(self, key):
        self.__key = key

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__key})"

    @property
    def key(self):
        return self.__key