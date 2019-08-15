from .data import Model
from ..base.pattern import Factory, Singleton, Pool
from ..base.pattern import LinkedNode, LinkedList

from collections import OrderedDict
from collections import defaultdict

class Component(Model, LinkedNode):
    def __init__(self, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)
        LinkedNode.__init__(self)
        self.__eid = 0

    def bind(self, eid):
        self.__eid = eid

    @property
    def eid(self):
        return self.__eid

class ComponentFactory(Factory, Singleton):
    def __init__(self):
        Factory.__init__(self)
        Singleton.__init__(self)
        self.__cid_comps = defaultdict(list)

    def create(self, cid):
        comps = self.__cid_comps[cid]
        if comps:
            return comps.pop()
        else:
            return Factory.create(self, cid)
            
    def destroy(self, cid, comp):
        comps = self.__cid_comps[cid]
        if comps:
            comps.append(comp)

class Entity:
    def __init__(self):
        self.__comps = {}

    def reset(self):
        if self.__comps:
            for comp in self.__comps.values():
                comp.kill_self()

            self.__comps = {}

        self.__eid = 0

    def add(self, cid, comp):
        self.__comps[cid] = comp

    def get(self, cid):
        return self.__comps.get(cid)

    @property
    def components(self):
        return self.__comps


class EntityPool(Pool):
    def __init__(self, ent_cap, **kwargs):
        Pool.__init__(self, ent_cap, **kwargs)
        self.__ents = [Entity() for idx in range(ent_cap)] 

    def get(self, handle):
        valid, idx = self.parse(handle)
        if valid:
            return self.__ents[idx]
        else:
            return None

class World:
    def __init__(self, ent_cap):
        self.__eid_ents = EntityPool(ent_cap)
        self.__cid_comps = defaultdict(LinkedList)

    def spawn(self, cids):
        eid = self.__eid_ents.alloc()
        ent = self.__eid_ents.get(eid)
        if not ent:
            return 0

        factory = ComponentFactory.get()
        for cid in cids:
            comp = factory.create(cid)
            comp.bind(eid)
            ent.add(cid, comp)
            self.__cid_comps[cid].push_back(comp)

        return eid

    def kill(self, eid):
        ent = self.__eid_ents.get(eid)
        if ent:
            factory = ComponentFactory.get()
            for cid, comp in ent.components.items():
                factory.destroy(cid, comp)

            ent.reset()
            self.__eid_ents.free(eid)

    def get_entity(self, eid):
        return self.__eid_ents.get(eid)

    def get_components(self, cid):
        return self.__cid_comps.get(cid)

class System:
    def __init__(self, world):
        self.__world = world

    @property
    def world(self):
        return self.__world


if __name__ == '__main__':
    from .data import Primitive
    from .data import String

    class Position(Primitive):
        def __init__(self, *args, **kwargs):
            Primitive.__init__(self, 'p', (0, 0, 0), *args, **kwargs)

    class Rotation(Primitive):
        def __init__(self, *args, **kwargs):
            Primitive.__init__(self, 'd', 0, *args, **kwargs) # 0: x+

    class Transform(Component):
        pos = Position()
        rot = Rotation()

    class Identity(Component):
        name = String()

    class TestSystem(System):
        def print_identities(self):
            for iden in world.get_components(CN.IDENTITY):
                print(f"{iden.eid}:{iden.name}")

        def print_transforms(self):
            for trans in world.get_components(CN.TRANSFORM):
                print(f"{trans.eid}:{trans.pos}")

    from enum import Enum

    class CN(Enum):
        IDENTITY = 1
        TRANSFORM = 2

    comp_factory = ComponentFactory.get()
    comp_factory.register(CN.IDENTITY, Identity)
    comp_factory.register(CN.TRANSFORM, Transform)

    world = World(100)
    eid1 = world.spawn([CN.IDENTITY, CN.TRANSFORM])
    ent1 = world.get_entity(eid1)
    ent1.get(CN.IDENTITY).name = 'A'
    ent1.get(CN.TRANSFORM).pos = Position(0, 0)
    print(eid1)

    eid2 = world.spawn([CN.IDENTITY, CN.TRANSFORM])
    ent2 = world.get_entity(eid2)
    ent2.get(CN.IDENTITY).name = 'B'
    ent2.get(CN.TRANSFORM).pos = Position(2, 0)
    print(eid2)

    eid3 = world.spawn([CN.IDENTITY, CN.TRANSFORM])
    ent3 = world.get_entity(eid3)
    ent3.get(CN.IDENTITY).name = 'C'
    ent3.get(CN.TRANSFORM).pos = Position(7, 0)
    print(eid3)

    eid4 = world.spawn([CN.TRANSFORM])
    ent4 = world.get_entity(eid4)
    ent4.get(CN.TRANSFORM).pos = Position(5, 0)
    print(eid4)

    world.kill(eid2)

    test_system = TestSystem(world)
    test_system.print_identities()
    test_system.print_transforms()