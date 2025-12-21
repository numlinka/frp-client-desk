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

# internal
from . import _common
from . import _options
from . import _proxies
from . import _terminal


class Minutiae (object):
    def __init__(self, master: "interface._services.Services") -> None:
        self.master = master
        self.frame = self.master.frame_minutiae
        self.frame_minutiae = ttkbootstrap.Frame(self.frame)
        self.frame_null = ttkbootstrap.Frame(self.frame)
        self.notebook = ttkbootstrap.Notebook(self.frame_minutiae)
        self.frame_options = ttkbootstrap.Frame(self.frame_minutiae)
        self.build()

    @once
    def build(self) -> None:
        self.frame_options.pack(side=BOTTOM, fill=X)
        self.notebook.pack(side=TOP, fill=BOTH, expand=True, pady=(0, 5))
        self.label_null = ttkbootstrap.Label(self.frame_null, text="minutiae.null", anchor=CENTER)
        self.label_null.pack(side=TOP, fill=BOTH, expand=True)
        self.options = _options.Options(self)
        self.terminal = _terminal.Terminal(self)
        self.common = _common.Common(self)
        self.proxies = _proxies.Proxies(self)
        self.hide()

    def show(self) -> None:
        self.frame_null.pack_forget()
        self.frame_minutiae.pack(side=TOP, fill=BOTH, expand=True)

    def hide(self) -> None:
        self.frame_minutiae.pack_forget()
        self.frame_null.pack(side=TOP, fill=BOTH, expand=True)

    def update(self) -> None:
        name = self.master.enumerate.item_selected
        self.options.update()

        if name is None or name == "$ /add":
            self.hide()
            return

        self.show()
        self.terminal.clear()
        self.common.config_clear()

        config = module.services.instance(name).load_config()
        proxys = config.get("proxies", [])
        if not isinstance(proxys, list): proxys = []
        start = config.get("start", [])
        if not isinstance(start, list): start = []

        self.terminal.update()
        self.common.config_update(config)
        self.proxies.config_update(proxys, start)
