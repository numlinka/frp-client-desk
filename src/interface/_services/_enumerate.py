# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

__all__ = ["Enumerate"]

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
                interface.methods.treeview_value_set(self.treeview, item, 1, i18n.UI.enum_c_delete if item != "$ /add" else i18n.UI.enum_c_create)

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
        self.master.minutiae.update()

    def create(self) -> None:
        name = dialogs.Querybox.get_string(title=i18n.UI.enum_new_ins, prompt=i18n.UI.enum_new_ins_t)
        if name is None: return
        name = name.strip()
        if not name:
            dialogs.Messagebox.show_error(title=i18n.UI.enum_new_ins_err, message=i18n.UI.enum_new_ins_err_t_null)
            return

        if name in module.services.instances_names():
            dialogs.Messagebox.show_error(title=i18n.UI.enum_new_ins_err, message=i18n.UI.enum_new_ins_err_t_exist)
            return

        for char in ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]:
            if char in name:
                dialogs.Messagebox.show_error(title=i18n.UI.enum_new_ins_err, message=i18n.UI.enum_new_ins_err_t_valid.format(char=char))
                return

        self.treeview.delete("$ /add")
        self.treeview.insert("", "end", iid=name, text=name)
        self.item_hover = None
        module.services.create(name)
        self.treeview.insert("", "end", iid=f"$ /add", text="")

    def delete(self, item: str) -> None:
        if module.services.instance(item).alive:
            dialogs.Messagebox.show_error(title=i18n.UI.enum_del_ins_err, message=i18n.UI.enum_del_ins_err_t)
            return

        result = dialogs.Messagebox.okcancel(title=i18n.UI.enum_del_ins, message=i18n.UI.enum_del_ins_t.format(item=item))
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
                interface.methods.treeview_value_set(self.treeview, name, 0, i18n.UI.enum_c_running)
            else:
                interface.methods.treeview_tag_remove(self.treeview, name, "running")
                interface.methods.treeview_value_set(self.treeview, name, 0, "")

        self.treeview.delete("$ /add")
        self.treeview.insert("", "end", iid=f"$ /add", text="")
