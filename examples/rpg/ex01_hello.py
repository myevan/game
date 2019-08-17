import os

from engine.core.ecs import System, EventHandler
from engine.core.events import EventNum, KeyNum, KeyEvent, KeyPressed
from engine.core.components import Cell
from engine.core.components import ComponentNum as CN

class EXPlayer(System, EventHandler):
    def __init__(self, world, eid):
        System.__init__(self, world)
        ent = world.get_entity(eid)
        cell = ent.get(CN.Cell)
        self.eid = eid
        self.ent = ent
        self.cell = cell

    def recv_event(self, evt):
        if isinstance(evt, KeyEvent):
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
           
if __name__ == '__main__':
    from engine.core.environment import Environment
    Environment.get().set_main_file_path(__file__)

    from engine.core.ecs import ComponentFactory
    comp_factory = ComponentFactory.get()
    comp_factory.register(CN.Cell, Cell)

    from engine.core.ecs import World
    world = World(100)
    eid = world.spawn([CN.Cell])
    ent = world.get_entity(eid)
    cell = ent.get(CN.Cell)
    cell.row = 30
    cell.col = 40
    cell.val = '@'

    from engine.core.systems.system_tcod import TCRenderer
    tc_renderer = TCRenderer(world)
    world.bind_event(EventNum.App, tc_renderer)

    ex_player = EXPlayer(world, eid)
    world.bind_event(EventNum.Key, ex_player)

    from engine.core.ecs import SystemManager
    sys_mgr = SystemManager(world)
    sys_mgr.add(ex_player)
    sys_mgr.add(tc_renderer)
    sys_mgr.run()
