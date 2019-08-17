import tcod
import os

from ..ecs import System, EventHandler
from ..environment import Environment

from ..events import KeyNum, KeyPressed
from ..components import Cell
from ..components import ComponentNum as CN

class TCView(System, EventHandler):
    VK_MAP = {
        tcod.KEY_ESCAPE: KeyNum.Escape,
        tcod.KEY_UP: KeyNum.Up,
        tcod.KEY_DOWN: KeyNum.Down,
        tcod.KEY_LEFT: KeyNum.Left,
        tcod.KEY_RIGHT: KeyNum.Right,
    }

    CH_MAP = {
        'k': KeyNum.Up,
        'j': KeyNum.Down,
        'h': KeyNum.Left,
        'l': KeyNum.Right,
    }

    def __init__(self, world, title):
        System.__init__(self, world)

        env = Environment.get()
        font_file_path = os.path.join(env.main_dir_path, 'arial10x10.png')
        tcod.console_set_custom_font(font_file_path, flags=tcod.FONT_TYPE_GREYSCALE|tcod.FONT_LAYOUT_TCOD)
        tcod.console_init_root(w=80, h=60, title=title, fullscreen=False)
        tcod.sys_set_fps(30)

    def update(self):
        if tcod.console_is_window_closed():
            self.world.close()
            return

        tcod.console_set_default_foreground(0, tcod.white)

        for cell in self.world.get_components(CN.Cell):
            tcod.console_put_char(0, cell.col, cell.row, cell.val, tcod.BKGND_NONE)

        tcod.console_flush()

        for cell in self.world.get_components(CN.Cell):
            tcod.console_put_char(0, cell.col, cell.row, ' ', tcod.BKGND_NONE)


        key = tcod.console_check_for_keypress()
        if key.vk != tcod.KEY_NONE:
            if key.vk == tcod.KEY_CHAR:
                ch = chr(key.c)
                key_num = self.CH_MAP.get(ch, KeyNum.Unknown)
                self.world.send_event(KeyPressed(key_num, repr(key)))
            else:
                key_num = self.VK_MAP.get(key.vk, KeyNum.Unknown)
                self.world.send_event(KeyPressed(key_num, repr(key)))

