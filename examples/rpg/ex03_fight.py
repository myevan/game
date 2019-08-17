from engine.core.environment import Environment
Environment.get().set_main_file_path(__file__)

from engine.core.ecs import ComponentFactory
comp_factory = ComponentFactory.get()

from engine.core.components import ComponentNum as CN
from engine.core.components import Cell
comp_factory.register(CN.Cell, Cell)

from engine.core.ecs import World
world = World(100)

from engine.core.systems.system_tcod import TCView
tc_view = TCView(world, "rpg")

from engine.core.ecs import SystemManager
sys_mgr = SystemManager(world)

from engine.core.events import EventNum
world.bind_event(EventNum.App, tc_view)
sys_mgr.add(tc_view)

from engine.core.ecs import System, EventHandler
class EXPlayer(System, EventHandler):
    def __init__(self, world, eid):
        System.__init__(self, world)
        ent = world.get_entity(eid)

        from engine.core.components import ComponentNum as CN
        cell = ent.get(CN.Cell)
        self.eid = eid
        self.ent = ent
        self.cell = cell

    def recv_event(self, evt):
        from engine.core.events import KeyEvent
        if isinstance(evt, KeyEvent):
            from engine.core.events import KeyNum
            if evt.key_num == KeyNum.Escape:
                self.world.close()
            elif evt.key_num == KeyNum.Up:
                self.cell.row -= 1
            elif evt.key_num == KeyNum.Down:
                self.cell.row += 1
            elif evt.key_num == KeyNum.Left:
                self.cell.col -= 1
            elif evt.key_num == KeyNum.Right:
                self.cell.col += 1

eid = world.spawn([CN.Cell])
ent = world.get_entity(eid)
cell = ent.get(CN.Cell)
cell.row = 30
cell.col = 40
cell.val = '@'
ex_player = EXPlayer(world, eid)
world.bind_event(EventNum.Key, ex_player)
sys_mgr.add(ex_player)

# EX03
eid = world.spawn([CN.Cell])
ent = world.get_entity(eid)
cell = ent.get(CN.Cell)
cell.row = 30
cell.col = 50
cell.val = 'm'
# EX03_END

sys_mgr.run()
