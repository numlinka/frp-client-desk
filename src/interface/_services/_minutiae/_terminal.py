# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

__all__ = ["Terminal"]

# site
import ttkbootstrap

from typex import once
from ttkbootstrap.constants import *

# local
import core
import module
import interface

from basic import i18n
from constants.event import INSTANCE_LOG_UPDATED


class Terminal (object):
    def __init__(self, master: "interface._services._minutiae.Minutiae") -> None:
        self.master = master
        self.frame = ttkbootstrap.Frame(self.master.notebook)
        self.master.notebook.add(self.frame, text=i18n.UI.terminal)
        self.build()

    @once
    def build(self) -> None:
        self.textbox = ttkbootstrap.Text(self.frame, wrap=NONE, state=DISABLED)
        self.scrollbar = ttkbootstrap.Scrollbar(self.frame, orient=VERTICAL, command=self.textbox.yview)
        self.textbox.configure(yscrollcommand=self.scrollbar.set)
        self.textbox.pack(side=LEFT, fill=BOTH, expand=True, padx=(2, 1), pady=2)
        self.scrollbar.pack(side=RIGHT, fill=Y, padx=(0, 2), pady=2)
        core.event.subscribe(INSTANCE_LOG_UPDATED, self.update_log)

    def clear(self) -> None:
        with self:
            self.textbox.delete("1.0", END)

    def print(self, text: str) -> None:
        _, last = self.textbox.yview()

        with self:
            self.textbox.insert(END, text)

        if last == 1.0:
            self.textbox.see(END)

    def println(self, text: str) -> None:
        self.print(text + "\n")

    def __enter__(self) -> "Terminal":
        self.textbox.configure(state=NORMAL)
        return self

    def __exit__(self, *_) -> None:
        self.textbox.configure(state=DISABLED)

    def update(self) -> None:
        name = self.master.master.enumerate.item_selected
        if name is None or name == "$ /add": return

        self.clear()
        module.services.instance(name).log_index_clear()
        self.update_log()

    def update_log(self) -> None:
        name = self.master.master.enumerate.item_selected
        if name is None or name == "$ /add": return
        lst = module.services.instance(name).log_pop()
        for log in lst:
            self.println(log)
