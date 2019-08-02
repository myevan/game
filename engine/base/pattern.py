class SingletonMeta(type):
    def __new__(meta, cls_name, bases, attrs):
        new_cls = type.__new__(meta, cls_name, bases, attrs)
        new_cls._inst = new_cls()
        return new_cls

class Singleton(metaclass=SingletonMeta):
    @classmethod
    def get(cls):
        return cls._inst

from collections import OrderedDict

class KeySingletonMeta(type):
    def __new__(meta, cls_name, bases, attrs):
        new_cls = type.__new__(meta, cls_name, bases, attrs)
        new_cls._insts = OrderedDict()
        return new_cls

class KeySingleton(metaclass=KeySingletonMeta):
    @classmethod
    def get(cls, key):
        return cls._insts.get(key)

    @classmethod
    def get_keys(cls):
        return cls._insts.keys()

    @classmethod
    def get_items(cls):
        return cls._insts.items()

    @classmethod
    def get_values(cls):
        return cls._insts.values()

    @classmethod
    def spawn(cls, key, *args, **kwargs):
        inst = cls(key, *args, **kwargs)
        cls._insts[key] = inst
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


from collections import defaultdict

class CacheMeta(type):
    def __new__(meta, cls_name, bases, attrs):
        new_cls = type.__new__(meta, cls_name, bases, attrs)
        new_cls._insts = defaultdict()
        return new_cls

class Cache(metaclass=CacheMeta):
    @classmethod
    def get(cls, key):
        inst = cls._insts.get(key)
        return inst if inst else cls.load(key)

    @classmethod
    def load(cls, key):
        inst = cls(key)
        cls._insts[key] = inst
        return inst

    def __init__(self, key):
        self.__key = key

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__key})"

    @property
    def key(self):
        return self.__key


if __name__ == '__main__':
    class TestA1(Singleton):
        def __init__(self):
            self.name = 'A1'

    class TestA2(Singleton):
        def __init__(self):
            self.name = 'A2'

    class TestB1(KeySingleton):
        pass

    class TestB2(KeySingleton):
        pass

    class TestC(Cache):
        def __init__(self, key):
            print(key)
            

    TestA1.get()
    print(TestA2.get().name)

    TestB1.spawn('1')
    print(TestB2.get('1'))

    TestC.get('x')
    TestC.get('x')