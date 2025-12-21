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

        self.options = []
        for i, info in enumerate(CONFIG_LIST):
            self.options.append(ConfigUnit(self.scrollframe, i, info))


class ConfigUnit (object):
    def __init__(self, master: ttkbootstrap.Frame, serial: int, info: ConfigOption) -> None:
        self.master = master
        self.serial = serial
        self.info = info
        self.build()

    def build(self) -> None:
        if self.info.type_ == int:      self.variable = ttkbootstrap.IntVar()
        elif self.info.type_ == bool:   self.variable = ttkbootstrap.BooleanVar()
        elif self.info.type_ == float:  self.variable = ttkbootstrap.DoubleVar()
        else:                           self.variable = ttkbootstrap.StringVar()

        self.label = ttkbootstrap.Label(self.master, text=self.info.name)

        match self.info.name:
            case "auth.method":
                self.entry = ttkbootstrap.Combobox(self.master, values=["", "token", "oidc"], width=50, textvariable=self.variable, state=READONLY)
                self.variable.set("token")

            case "serverPort" | "webServer.port":
                self.entry = ttkbootstrap.Spinbox(self.master, from_=0, to=65535, width=50, textvariable=self.variable)

            case "udpPacketSize":
                self.entry = ttkbootstrap.Spinbox(self.master, from_=0, to=65535, width=50, textvariable=self.variable)
                self.variable.set(1500)

            case _:
                if self.info.type_ == bool:
                    self.entry = ttkbootstrap.Checkbutton(self.master, variable=self.variable, text="False / True", bootstyle=(SQUARE, TOGGLE))

                else:
                    self.entry = ttkbootstrap.Entry(self.master, width=50, textvariable=self.variable)

        self.label.grid(row=self.serial, column=0, sticky=W, padx=2, pady=2)
        self.entry.grid(row=self.serial, column=1, sticky=EW, padx=2, pady=2)
        interface.annotation.register(self.label, i18n.ctrl.translation(f"description.frp.{self.info.name}"))
        interface.annotation.register(self.entry, i18n.ctrl.translation(f"description.frp.{self.info.name}"))
