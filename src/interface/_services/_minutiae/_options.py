# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

# std
import tkinter

# site
import ttkbootstrap

from typex import once
from ttkbootstrap import dialogs
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
        self.button_reload = ttkbootstrap.Button(self.frame, text="reload", bootstyle=(PRIMARY, OUTLINE), command=self.bin_reload, width=12)
        self.button_save = ttkbootstrap.Button(self.frame, text="save", bootstyle=(INFO, OUTLINE), command=self.bin_save, width=12)
        self.button_switch.pack(side=RIGHT)
        self.button_reload.pack(side=RIGHT, padx=(0, 4))
        self.button_save.pack(side=RIGHT, padx=(0, 4))

    def sbin_disabled(self) -> None:
        self.button_switch.configure(state=DISABLED)
        self.button_reload.configure(state=DISABLED)
        self.button_save.configure(state=DISABLED)
        interface.mainwindow.update()

    def sbin_enabled(self) -> None:
        self.button_switch.configure(state=NORMAL)
        self.button_reload.configure(state=NORMAL)
        self.button_save.configure(state=NORMAL)

    def bin_switch(self) -> None:
        self.sbin_disabled()
        interface.services.minutiae.terminal.clear()
        interface.mainwindow.after(500, self.sbin_enabled)

    def bin_reload(self) -> None:
        self.sbin_disabled()
        name = self.master.master.enumerate.item_selected
        if name is None or name == f"$ /add": return
        module.services.instance(name).reload()
        interface.mainwindow.after(500, self.sbin_enabled)

    def bin_save(self) -> None:
        self.sbin_disabled()
        if not self.master.common.validity:
            dialogs.Messagebox.show_warning(title="参数错误", message="通用配置存在参数错误\n请检查被颜色标记的参数")
            return

        if not self.master.proxies.validity:
            dialogs.Messagebox.show_warning(title="参数错误", message="隧道列表存在参数错误\n请检查被颜色标记的参数")
            return

        name = self.master.master.enumerate.item_selected
        if name is None or name == f"$ /add": return
        config = self.master.common.config_get()
        proxies, start = self.master.proxies.config_get()
        config["start"] = start
        config["proxies"] = proxies
        module.services.instance(name).save_config(config)
        interface.mainwindow.after(500, self.sbin_enabled)

    def update(self) -> None:
        name = self.master.master.enumerate.item_selected
        if name is None or name == f"$ /add":
            return

        instance = module.services.instance(name)
        if instance.alive:
            self.button_switch.configure(text="■ 停止", bootstyle=(DANGER, OUTLINE))
        else:
            self.button_switch.configure(text="▶ 启动", bootstyle=(SUCCESS, OUTLINE))
