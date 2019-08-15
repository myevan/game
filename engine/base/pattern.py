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

class LinkedNode:
    def __init__(self):
        self.__next_node = None
        self.__prev_node = None

    def link_next(self, node):
        self.__next_node = node
        node.__prev_node = self

    def link_prev(self, node):
        self.__prev_node = node
        node.__next_node = self

    def kill_self(self):
        next_node = self.__next_node
        prev_node = self.__prev_node

        if prev_node:
            prev_node.__next_node = next_node

        if next_node:
            next_node.__prev_node = prev_node

        self.__next_node = None
        self.__prev_node = None

    @property
    def next(self):
        return self.__next_node

    @property
    def prev(self):
        return self.__next_node

class LinkedRange:
    def __init__(self, node):
        self.__node = node

    def __iter__(self):
        return self

    def __next__(self):
        ret = self.__node
        if ret == None:
            raise StopIteration

        self.__node = ret.next
        return ret

class LinkedList:
    def __init__(self):
        self.__head = None
        self.__tail = None

    def push_front(self, node):
        if self.__head is None:
            self.__head = node
            self.__tail = node
        else:
            self.__head.link_prev(node)
            self.__head = node

    def __iter__(self):
        return LinkedRange(self.__head)

    def push_back(self, node):
        if self.__head is None:
            self.__head = node
            self.__tail = node
        else:
            self.__tail.link_next(node)
            self.__tail = node

    def pop_front(self):
        if self.__head is None:
            return None
        else:
            ret = self.__head
            self.__head.kill_self()
            return ret

    def pop_back(self):
        if self.__tail is None:
            return None
        else:
            ret = self.__tail
            self.__tail.kill_self()
            return ret

class Pool:
    def __init__(self, idx_cap, seq_cap=1000, seq_base=1000):
        self.chks = [None] * idx_cap
        self.free_idxs = list(range(idx_cap))
        self.free_idxs.reverse()
        self.idx_cap = idx_cap
        self.seq_base = seq_base
        self.seq_cap = seq_cap
        self.seq_idx = 1

    def alloc(self):
        if not self.free_idxs:
            return 0

        chk = self.seq_base + self.seq_idx
        self.seq_idx += 2
        self.seq_idx %= self.seq_cap

        idx = self.free_idxs.pop()
        self.chks[idx] = chk
        return chk * self.idx_cap + idx

    def free(self, handle):
        valid, idx = self.parse(handle)
        if valid:
            self.chks[idx] = None
            self.free_idxs.append(idx)

    def parse(self, handle):
        chk = handle // self.idx_cap
        idx = handle % self.idx_cap
        return chk == self.chks[idx], idx


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

    test_node1 = LinkedNode()
    test_node2 = LinkedNode()
    test_node3 = LinkedNode()
    test_list = LinkedList()
    test_list.push_back(test_node2)
    test_list.push_back(test_node3)
    test_list.push_front(test_node1)
    for each_node in test_list: pass
    test_node2.kill_self()
    test_list.pop_front()
    test_list.pop_back()

    pool = Pool(1000)
    oid1 = pool.alloc()
    print(oid1)
    oid2 = pool.alloc()
    print(oid2)
    pool.free(oid1)
    pool.free(oid2)