# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

# std
import webbrowser
from typing import Optional

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
    # ConfigOption("udpPacketSize", int),
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

    @property
    def validity(self) -> bool:
        return all(unit.validity for unit in self.options.values())

    @once
    def build(self) -> None:
        self.scrollframe.pack(side=TOP, fill=BOTH, expand=True, padx=2, pady=2)

        self.options: dict[str, ConfigUnit] = {}
        for i, info in enumerate(CONFIG_LIST):
            self.options[info.name] = ConfigUnit(self.scrollframe, i, info)

    def config_clear(self) -> None:
        for _, unit in self.options.items():
            unit.clear()

    def config_update(self, config: dict) -> None:
        for name, unit in self.options.items():
            if "." in name:
                k1, k2 = name.split(".")
                if k1 not in config: continue
                if k2 not in config[k1]: continue
                unit.variable.set(config[k1][k2])

            elif name in config:
                unit.variable.set(config[name])

    def config_get(self) -> dict:
        config = {}
        for name, unit in self.options.items():
            if "." in name:
                k1, k2 = name.split(".")
                if k1 not in config: config[k1] = {}
                config[k1][k2] = unit.get()

            else:
                config[name] = unit.get()

        return config


class ConfigUnit (object):
    def __init__(self, master: ttkbootstrap.Frame, serial: int, info: ConfigOption) -> None:
        self.master = master
        self.serial = serial
        self.info = info
        self.validity = True
        self.build()

    def build(self) -> None:
        self.variable = ttkbootstrap.Variable()

        self.label = ttkbootstrap.Label(self.master, text=self.info.name)

        width = 32
        match self.info.name:
            case "auth.method":
                self.entry = ttkbootstrap.Combobox(self.master, values=["", "token", "oidc"], width=width, textvariable=self.variable, state=READONLY)

            case "serverPort" | "webServer.port":
                self.entry = ttkbootstrap.Spinbox(self.master, from_=0, to=65535, width=width, textvariable=self.variable)

            case "udpPacketSize":
                self.entry = ttkbootstrap.Spinbox(self.master, from_=0, to=65535, width=width, textvariable=self.variable)

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

        self.variable.trace_add("write", self.bin_change)

    def bin_change(self, *_) -> None:
        value = self.variable.get()
        validity = False

        match self.info.name:
            case "auth.method":
                validity = value in ["", "token", "oidc"]

            case "serverPort" | "webServer.port":
                if value:
                    try:
                        value = int(value)
                        if 0 <= value <= 65535:
                            validity = True

                    except Exception:
                        pass

                else:
                    validity = True

            case _:
                validity = True

        self.validity = validity
        self.entry.configure(bootstyle=(DEFAULT if validity else DANGER))

    def clear(self) -> None:
        self.variable.set("")

    def set(self, value) -> None:
        self.variable.set(value)

    def get(self) -> Optional[str | int | bool]:
        value = self.variable.get()
        if not value: return None
        if self.info.type_ == bool:
            return bool(int(value))
        return self.info.type_(value)

    def open_browser(self) -> None:
        port = self.variable.get()
        if port == 0: return
        webbrowser.open(f"http://localhost:{port}")
