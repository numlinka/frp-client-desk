# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

# std
import webbrowser
from typing import Any

# site
import ttkbootstrap

from typex import once
from ttkbootstrap.constants import *

# local
import module
import interface

from basic import i18n
from widgets import ScrollFrame
from typeins import ConfigOption


CONFIG_LIST = [
    ConfigOption("auth.method", str),
    # ConfigOption("auth.additionalScopes", list[str]),
    ConfigOption("auth.token", str),
    ConfigOption("user", str),
    ConfigOption("serverAddr", str),
    ConfigOption("serverPort", int),
    ConfigOption("natHoleStunServer", str),
    ConfigOption("dnsServer", str),
    ConfigOption("loginFailExit", bool),
    # ConfigOption("start", list[str]),
    ConfigOption("webServer.addr", str),
    ConfigOption("webServer.port", int, "", True),
    ConfigOption("webServer.user", str),
    ConfigOption("webServer.password", str),
    ConfigOption("webServer.assetsDir", str),
    ConfigOption("webServer.pprofEnable", bool),
    # ConfigOption("webServer.tls", ...),
    ConfigOption("udpPacketSize", int),
    # ConfigOption("metadatas", dict[str, str]),
    # ConfigOption("includes", list[str]),
]


class Common (object):
    def __init__(self, master: "interface._services._minutiae.Minutiae") -> None:
        self.master = master
        self.frame = ttkbootstrap.Frame(self.master.notebook)
        self.master.notebook.add(self.frame, text=i18n.ctrl.translation("通用配置"))
        self.scrollframe = ScrollFrame(self.frame)
        self.build()

    @once
    def build(self) -> None:
        self.scrollframe.pack(side=TOP, fill=BOTH, expand=True, padx=2, pady=2)

        self.options: dict[str, ConfigUnit] = {}
        for i, info in enumerate(CONFIG_LIST):
            self.options[info.name] = ConfigUnit(self.scrollframe, i, info)

    def clear(self) -> None:
        for _, value in self.options.items():
            value.clear()

    def update(self, config: dict) -> None:
        # name = self.master.master.enumerate.item_selected
        # if name is None or name == "$ /add": return

        # config = module.services.instance(name).load_config()

        for name, value in self.options.items():
            if "." in name:
                k1, k2 = name.split(".")
                if k1 not in config: continue
                if k2 not in config[k1]: continue
                value.variable.set(config[k1][k2])

            elif name in config:
                value.variable.set(config[name])


class ConfigUnit (object):
    def __init__(self, master: ttkbootstrap.Frame, serial: int, info: ConfigOption) -> None:
        self.master = master
        self.serial = serial
        self.info = info
        self.build()

    def build(self) -> None:
        self.variable = ttkbootstrap.Variable()

        self.label = ttkbootstrap.Label(self.master, text=self.info.name)

        width = 32
        match self.info.name:
            case "auth.method":
                self.entry = ttkbootstrap.Combobox(self.master, values=["", "token", "oidc"], width=width, textvariable=self.variable, state=READONLY)
                # self.variable.set("token")

            case "serverPort" | "webServer.port":
                self.entry = ttkbootstrap.Spinbox(self.master, from_=0, to=65535, width=width, textvariable=self.variable)

            case "udpPacketSize":
                self.entry = ttkbootstrap.Spinbox(self.master, from_=0, to=65535, width=width, textvariable=self.variable)
                # self.variable.set(1500)

            case _:
                if self.info.type_ == bool:
                    self.entry = ttkbootstrap.Checkbutton(self.master, variable=self.variable, text="False / True", bootstyle=(SQUARE, TOGGLE))

                else:
                    self.entry = ttkbootstrap.Entry(self.master, width=width, textvariable=self.variable)

        self.label.grid(row=self.serial, column=0, sticky=W, padx=2, pady=2)
        self.entry.grid(row=self.serial, column=1, sticky=EW, padx=2, pady=2)
        interface.annotation.register(self.label, i18n.ctrl.translation(f"description.frp.{self.info.name}"))
        interface.annotation.register(self.entry, i18n.ctrl.translation(f"description.frp.{self.info.name}"))

        if self.info.name == "webServer.port":
            self.button = ttkbootstrap.Button(self.master, text="➤", bootstyle=(OUTLINE, INFO), command=self.open_browser)
            self.button.grid(row=self.serial, column=2, sticky=E, padx=2, pady=2)
            interface.annotation.register(self.button, i18n.ctrl.translation(f"在浏览器中打开"))

    def clear(self) -> None:
        self.variable.set("")

    def open_browser(self) -> None:
        port = self.variable.get()
        if port == 0: return
        webbrowser.open(f"http://localhost:{port}")
