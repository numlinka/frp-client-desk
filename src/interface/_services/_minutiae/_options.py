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
import core
import module
import interface
from constants.event import INSTANCE_SWITCHED
from basic import i18n


class Options (object):
    def __init__(self, master: "interface._services._minutiae.Minutiae") -> None:
        self.master = master
        self.frame = self.master.frame_options
        self.labelframe = ttkbootstrap.Labelframe(self.frame, text=i18n.options)
        self.build()

    @once
    def build(self) -> None:
        self.labelframe.pack(fill=X)
        self.button_switch = ttkbootstrap.Button(self.labelframe, text="■ 停止", bootstyle=(DANGER, OUTLINE), command=self.bin_switch, width=12)
        self.button_reload = ttkbootstrap.Button(self.labelframe, text="reload", bootstyle=(INFO, OUTLINE), command=self.bin_reload, width=12)
        self.button_save = ttkbootstrap.Button(self.labelframe, text="save", bootstyle=(INFO, OUTLINE), command=self.bin_save, width=12)
        self.button_switch.pack(side=RIGHT, pady=4, padx=(4))
        self.button_reload.pack(side=RIGHT, pady=4, padx=(4, 0))
        self.button_save.pack(side=RIGHT, pady=4, padx=(4, 0))
        core.event.subscribe(INSTANCE_SWITCHED, self.update)

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
        name = self.master.master.enumerate.item_selected
        if name is None or name == f"$ /add": return
        instance = module.services.instance(name)
        instance.stop() if instance.alive else instance.run()
        interface.mainwindow.after(500, self.sbin_enabled)

    def bin_reload(self) -> None:
        self.sbin_disabled()
        name = self.master.master.enumerate.item_selected
        if name is None or name == f"$ /add": return
        module.services.instance(name).reload()
        interface.mainwindow.after(500, self.sbin_enabled)

    def bin_save(self) -> None:
        if not self.master.common.validity:
            dialogs.Messagebox.show_warning(title="参数错误", message="通用配置存在参数错误\n请检查被颜色标记的参数")
            return

        if not self.master.proxies.validity:
            dialogs.Messagebox.show_warning(title="参数错误", message="隧道列表存在参数错误\n请检查被颜色标记的参数")
            return

        self.sbin_disabled()
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
