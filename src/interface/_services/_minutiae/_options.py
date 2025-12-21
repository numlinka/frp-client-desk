# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

# std
import tkinter

# site
import ttkbootstrap

from typex import once
from ttkbootstrap.constants import *

# local
import module
import interface
from basic import i18n


class Options (object):
    def __init__(self, master: "interface._services._minutiae.Minutiae") -> None:
        self.master = master
        self.frame = self.master.frame_options
        self.build()

    @once
    def build(self) -> None:
        self.button_switch = ttkbootstrap.Button(self.frame, text="■ 停止", bootstyle=(DANGER, OUTLINE), command=self.bin_switch, width=12)
        self.button_reload = ttkbootstrap.Button(self.frame, text="reload", bootstyle=(WARNING, OUTLINE), command=self.bin_reload, width=12)
        self.button_refresh = ttkbootstrap.Button(self.frame, text="refresh", bootstyle=(INFO, OUTLINE), command=self.bin_refresh, width=12)
        self.button_switch.pack(side=RIGHT)
        self.button_reload.pack(side=RIGHT, padx=(0, 4))
        self.button_refresh.pack(side=RIGHT, padx=(0, 4))

    def bin_switch(self) -> None:
        interface.services.minutiae.terminal.clear()

    def bin_reload(self) -> None:
        interface.services.minutiae.terminal.println("reload")

    def bin_refresh(self) -> None:
        interface.services.minutiae.terminal.print("refresh ")

    def update(self) -> None:
        name = self.master.master.enumerate.item_selected
        if name is None or name == f"$ /add":
            return

        instance = module.services.instance(name)
        if instance.alive:
            self.button_switch.configure(text="■ 停止", bootstyle=(DANGER, OUTLINE))
        else:
            self.button_switch.configure(text="▶ 启动", bootstyle=(SUCCESS, OUTLINE))
