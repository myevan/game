from engine.core.environment import Environment
Environment.get().set_main_file_path(__file__)

from engine.core.ecs import ComponentFactory
comp_factory = ComponentFactory.get()

from engine.core.components import ComponentNum as CN
from engine.core.components import Cell
comp_factory.register(CN.Cell, Cell)

from engine.core.ecs import World
world = World(100)
eid = world.spawn([CN.Cell])
ent = world.get_entity(eid)
cell = ent.get(CN.Cell)
cell.row = 30
cell.col = 40
cell.val = '@'

from engine.core.ecs import SystemManager
sys_mgr = SystemManager(world)

from engine.core.systems.system_tcod import TCView
tc_view = TCView(world, "rpg")
sys_mgr.add(tc_view)

from engine.core.events import EventNum
world.bind_event(EventNum.App, tc_view)

sys_mgr.run()
