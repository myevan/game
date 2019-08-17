import logging
logging.basicConfig(level=logging.INFO)

from engine.core.environment import Environment
Environment.get().set_main_file_path(__file__)

from engine.core.ecs import ComponentFactory
comp_factory = ComponentFactory.get()

from engine.core.components import ComponentNum as CN
# EX04
from enum import Enum
class EN(Enum):
    Health = CN.Custom.value + 1

from engine.core.components import Component
from engine.core.primitives import Integer
class Health(Component):
    cur = Integer()
    cap = Integer()

comp_factory.register(EN.Health, Health)
# EX04_END

from engine.core.components import Cell
comp_factory.register(CN.Cell, Cell)

from engine.core.components import NumGrid
comp_factory.register(CN.NumGrid, NumGrid)

from engine.core.ecs import World
world = World(100)

eid = world.spawn([CN.NumGrid])
ent = world.get_entity(eid)
grid = ent.get(CN.NumGrid)
grid.create(80, 60)

from engine.core.ecs import SystemManager
sys_mgr = SystemManager(world)

from engine.core.systems.system_tcod import TCView
tc_view = TCView(world, "rpg")
sys_mgr.add(tc_view)

from engine.core.events import EventNum
world.bind_event(EventNum.App, tc_view)

from engine.core.ecs import System, EventHandler
class EXEntityManager(System, EventHandler):
    def __init__(self, world):
        System.__init__(self, world)

        self.grid = self.world.get_component(CN.NumGrid)

    def start(self):
        for cell in self.world.get_components(CN.Cell):
            self.grid.set(cell.row, cell.col, cell.eid)

ex_ent_mgr = EXEntityManager(world)
sys_mgr.add(ex_ent_mgr)

eid = world.spawn([CN.Cell])
ent = world.get_entity(eid)
cell = ent.get(CN.Cell)
cell.row = 30
cell.col = 40
cell.val = '@'

from engine.core.ecs import System, EventHandler
class EXPlayer(System, EventHandler):
    def __init__(self, world, eid):
        System.__init__(self, world)
        ent = world.get_entity(eid)
        cell = ent.get(CN.Cell)
        self.eid = eid
        self.ent = ent
        self.cell = cell
        self.grid = self.world.get_component(CN.NumGrid)

    def recv_event(self, evt):
        from engine.core.events import KeyEvent
        if isinstance(evt, KeyEvent):
            from engine.core.events import KeyNum
            if evt.key_num == KeyNum.Escape:
                self.world.close()
            elif evt.key_num == KeyNum.Up:
                self.move(0, -1)
            elif evt.key_num == KeyNum.Down:
                self.move(0, +1)
            elif evt.key_num == KeyNum.Left:
                self.move(-1, 0)
            elif evt.key_num == KeyNum.Right:
                self.move(+1, 0)

    def move(self, dx, dy):
        src_row = self.cell.row
        src_col = self.cell.col
        dst_row = self.cell.row + dy
        dst_col = self.cell.col + dx

        dst_eid = self.grid.get(dst_row, dst_col)
        if dst_eid != 0:
            # EX04
            dst_ent = self.world.get_entity(dst_eid)
            dst_health = dst_ent.get(EN.Health)
            dam = 1
            dst_health.cur -= dam
            if dst_health.cur > 0:
                logging.info(f"E{self.eid}.attack(dam={dam}) -> E{dst_eid}(hp={dst_health.cur}/{dst_health.cap})")
            else:
                logging.info(f"E{self.eid}.kill(dam={dam}) -> E{dst_eid}(hp={dst_health.cur}/{dst_health.cap})")
                self.world.kill(dst_eid)
                self.grid.set(dst_row, dst_col, 0)
            # EX04_END
            return

        self.grid.set(src_row, src_col, 0)
        self.grid.set(dst_row, dst_col, self.eid)

        self.cell.row = dst_row
        self.cell.col = dst_col

ex_player = EXPlayer(world, eid)
world.bind_event(EventNum.Key, ex_player)
sys_mgr.add(ex_player)

eid = world.spawn([CN.Cell, EN.Health]) # EX04
ent = world.get_entity(eid)
cell = ent.get(CN.Cell)
cell.row = 30
cell.col = 50
cell.val = 'm'
# EX04
health = ent.get(EN.Health)
health.cap = 2
health.cur = 2
# EX04_END

sys_mgr.run()
