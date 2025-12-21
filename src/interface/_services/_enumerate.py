# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

# std
import tkinter

# site
import ttkbootstrap

from typex import once
from ttkbootstrap import dialogs
from ttkbootstrap.constants import *
from ttkbootstrap.localization.msgcat import MessageCatalog

# local
import core
import module
from constants.event import INSTANCE_SWITCHED
import interface
from basic import i18n


class Enumerate (object):
    def __init__(self, master: "interface._services.Services") -> None:
        self.master = master
        self.frame = self.master.frame_enumerate
        self.build()

    @once
    def build(self) -> None:
        self.treeview = ttkbootstrap.Treeview(self.frame, show=TREE, columns=("#1", "#2"), selectmode=BROWSE)
        self.treeview.pack(side=TOP, fill=BOTH, expand=True)

        self.treeview.column("#0", width=150)
        self.treeview.column("#1", width=0)
        self.treeview.column("#2", width=0)

        # ▶ ⏸ ■ ⚠ ✎ ✚ ✖
        self.treeview.tag_configure("hover", background="lightgray")
        self.treeview.tag_configure("running", foreground="green")
        self.treeview.tag_configure("stop", foreground="gray")
        self.treeview.tag_configure("error", foreground="red")
        self.treeview.tag_configure("warning", foreground="orange")

        self.treeview.bind("<Motion>", self.bin_motion)
        self.treeview.bind("<Leave>", self.bin_leave)
        self.treeview.bind("<Button-1>", self.bin_click)
        self.treeview.bind("<<TreeviewSelect>>", self.bin_select)

        self.treeview.insert("", "end", iid=f"$ /add")

        self.item_hover = None
        self.item_selected = None
        core.event.subscribe(INSTANCE_SWITCHED, self.update)

    def bin_motion(self, event: tkinter.Event) -> None:
        item = self.treeview.identify_row(event.y)

        if item != self.item_hover:
            if self.item_hover:
                interface.methods.treeview_tag_remove(self.treeview, self.item_hover, "hover")
                interface.methods.treeview_value_set(self.treeview, self.item_hover, 1, "")
            self.item_hover = item

            if item:
                interface.methods.treeview_tag_add(self.treeview, item, "hover")
                interface.methods.treeview_value_set(self.treeview, item, 1, "✖" if item != "$ /add" else "✚")

        if item and self.treeview.identify_column(event.x) == "#2":
            self.treeview.configure(cursor="hand2")

        else:
            self.treeview.configure(cursor="")

    def bin_leave(self, _: tkinter.Event) -> None:
        if self.item_hover:
            interface.methods.treeview_tag_remove(self.treeview, self.item_hover, "hover")
            interface.methods.treeview_value_set(self.treeview, self.item_hover, 1, "")

        self.item_hover = None
        self.treeview.configure(cursor="")

    def bin_click(self, event: tkinter.Event) -> None:
        item = self.treeview.identify_row(event.y)
        column = self.treeview.identify_column(event.x)

        if not item or column != "#2":
            return

        if item == "$ /add":
            self.create()
            return

        self.delete(item)
        self.item_hover = None

    def bin_select(self, _: tkinter.Event) -> None:
        selection = self.treeview.selection()
        if not selection: return
        selected = selection[0]
        if self.item_selected == selected: return
        self.item_selected = selected
        # core.event.emit(constants.event.INSTANCE_SELECTED)
        self.master.minutiae.update()

    def create(self) -> None:
        name = dialogs.Querybox.get_string(title="新建实例", prompt="输入新的实例名称\n名称不能为空、不能重复、不能包含特殊字符")
        if name is None: return
        name = name.strip()
        if not name:
            dialogs.Messagebox.show_error(title="创建实例失败", message="非法的实例名称\n实例名称不能为空")
            return

        for char in ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]:
            if char in name:
                dialogs.Messagebox.show_error(title="创建实例失败", message=f"非法的实例名称\n实例名称不能包含特殊字符：{char}")
                return

        self.treeview.delete("$ /add")
        self.treeview.insert("", "end", iid=name, text=name)
        self.item_hover = None
        module.services.create(name)
        self.treeview.insert("", "end", iid=f"$ /add", text="")

    def delete(self, item: str) -> None:
        if module.services.instance(item).alive:
            dialogs.Messagebox.show_error(title="删除实例失败", message="不可删除正在运行实例\n请先停止该实例")
            return

        result = dialogs.Messagebox.okcancel(title="删除实例", message=f"确定删除实例 {item} 吗？\n这将删除实例的所有配置和数据")
        if result != MessageCatalog.translate("OK"): return
        module.services.delete(item)
        self.treeview.delete(item)

    def update(self) -> None:
        names = module.services.instances_names()

        for name in names:
            instance = module.services.instance(name)
            if not self.treeview.exists(name):
                self.treeview.insert("", "end", iid=name, text=name)
            if instance.alive:
                interface.methods.treeview_tag_add(self.treeview, name, "running")
                interface.methods.treeview_value_set(self.treeview, name, 0, "▶")
            else:
                interface.methods.treeview_tag_remove(self.treeview, name, "running")
                interface.methods.treeview_value_set(self.treeview, name, 0, "")

        self.treeview.delete("$ /add")
        self.treeview.insert("", "end", iid=f"$ /add", text="")
