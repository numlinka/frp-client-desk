# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

# std
import tkinter

# site
import ttkbootstrap

from typex import once
from ttkbootstrap.constants import *

# local
import interface
from basic import i18n


class Terminal (object):
    def __init__(self, master: "interface._services._minutiae.Minutiae") -> None:
        self.master = master
        self.frame = ttkbootstrap.Frame(self.master.notebook)
        self.master.notebook.add(self.frame, text=i18n.ctrl.translation("终端"))
        self.build()

    @once
    def build(self) -> None:
        self.textbox = ttkbootstrap.Text(self.frame, wrap=NONE, state=DISABLED)
        self.scrollbar = ttkbootstrap.Scrollbar(self.frame, orient=VERTICAL, command=self.textbox.yview)
        self.textbox.configure(yscrollcommand=self.scrollbar.set)
        self.textbox.pack(side=LEFT, fill=BOTH, expand=True, padx=(2, 1), pady=2)
        self.scrollbar.pack(side=RIGHT, fill=Y, padx=(0, 2), pady=2)

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
