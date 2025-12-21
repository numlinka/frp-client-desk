# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

__all__ = ["Proxies"]

# site
import ttkbootstrap

from typex import Atomic, once
from ttkbootstrap import dialogs
from ttkbootstrap.constants import *

# local
import interface

from basic import i18n
from widgets import ScrollFrame


class Proxies (object):
    def __init__(self, master: "interface._services._minutiae.Minutiae") -> None:
        self.master = master
        self.frame = ttkbootstrap.Frame(self.master.notebook)
        self.master.notebook.add(self.frame, text=i18n.UI.proxies)
        self.scrollframe = ScrollFrame(self.frame)
        self.build()

    @property
    def validity(self) -> bool:
        return all(unit.validity for unit in self.list)

    @once
    def build(self) -> None:
        self.scrollframe.pack(side=TOP, fill=BOTH, expand=True, padx=2, pady=2)
        self.atomic = Atomic()
        self.atomic.get_count()

        self.lable_name = ttkbootstrap.Label(self.scrollframe, text=i18n.UI.proxies_name)
        self.lable_type = ttkbootstrap.Label(self.scrollframe, text=i18n.UI.proxies_type)
        self.lable_local_ip = ttkbootstrap.Label(self.scrollframe, text=i18n.UI.proxies_local_ip)
        self.lable_local_port = ttkbootstrap.Label(self.scrollframe, text=i18n.UI.proxies_local_port)
        self.lable_remote_port = ttkbootstrap.Label(self.scrollframe, text=i18n.UI.proxies_remote_port)
        self.lable_enable = ttkbootstrap.Label(self.scrollframe, text=i18n.UI.proxies_enable)
        self.lable_delete = ttkbootstrap.Label(self.scrollframe, text=i18n.UI.proxies_delete)
        self.button_add = ttkbootstrap.Button(self.scrollframe, text=i18n.UI.proxies_add, bootstyle=(SUCCESS, OUTLINE), command=self.bin_add_proxy)

        self.lable_name.grid(row=0, column=0, sticky=EW, padx=2, pady=2)
        self.lable_type.grid(row=0, column=1, sticky=EW, padx=2, pady=2)
        self.lable_local_ip.grid(row=0, column=2, sticky=EW, padx=2, pady=2)
        self.lable_local_port.grid(row=0, column=3, sticky=EW, padx=2, pady=2)
        self.lable_remote_port.grid(row=0, column=4, sticky=EW, padx=2, pady=2)
        self.lable_enable.grid(row=0, column=5, sticky=EW, padx=2, pady=2)
        self.lable_delete.grid(row=0, column=6, sticky=EW, padx=2, pady=2)
        self.button_add.grid(row=9998, column=0, sticky=W, padx=2, pady=2)

        self.list: list[ConfigUnit] = []
        self.bin_add_proxy()

    def get_all_proxy_names(self) -> list[str]:
        return [i.v_name.get() for i in self.list]

    def bin_add_proxy(self, *_) -> None:
        self.list.append(ConfigUnit(self, self.atomic.count))

    def bin_delete_proxy(self, unit: "ConfigUnit") -> None:
        if len(self.list) == 1:
            dialogs.Messagebox.show_error(title=i18n.UI.proxies_del_err, message=i18n.UI.proxies_del_err_t)
            return

        self.list.remove(unit)
        unit.forget()

    def config_clear(self) -> None:
        self.atomic = Atomic()
        self.atomic.get_count()
        for unit in self.list:
            unit.forget()
        self.list.clear()

    def config_update(self, proxys: list[dict], start: list[str]) -> None:
        for unit in self.list:
            unit.forget()
        self.list.clear()

        if not proxys:
            self.list.append(ConfigUnit(self, self.atomic.count))

        for proxy in proxys:
            unit = ConfigUnit(self, self.atomic.count)
            self.list.append(unit)
            if "name" in proxy: unit.v_name.set(proxy["name"])
            if "type" in proxy: unit.v_type.set(proxy["type"])
            if "localIP" in proxy: unit.v_local_ip.set(proxy["localIP"])
            if "localPort" in proxy: unit.v_local_port.set(proxy["localPort"])
            if "remotePort" in proxy: unit.v_remote_port.set(proxy["remotePort"])
            if not start or ("name" in proxy and proxy["name"] in start):
                unit.v_enable.set(True)
            else:
                unit.v_enable.set(False)

    def config_get(self) -> tuple[list[dict], list[str]]:
        proxys = []
        start = []

        for unit in self.list:
            proxys.append({
                "name": unit.v_name.get(),
                "type": unit.v_type.get(),
                "localIP": unit.v_local_ip.get(),
                "localPort": int(unit.v_local_port.get()),
                "remotePort": int(unit.v_remote_port.get()),
            })

            if unit.v_enable.get():
                start.append(unit.v_name.get())

        return proxys, start


class ConfigUnit (object):
    def __init__(self, master: Proxies, serial: int) -> None:
        self.master = master
        self.frame = self.master.scrollframe
        self.serial = serial
        self.__validity: list[bool] = [False] * 5
        self.build()

    @property
    def validity(self) -> bool:
        return all(self.__validity)

    def build(self) -> None:
        self.v_name = ttkbootstrap.StringVar()
        self.v_type = ttkbootstrap.StringVar()
        self.v_local_ip = ttkbootstrap.StringVar()
        self.v_local_port = ttkbootstrap.Variable()
        self.v_remote_port = ttkbootstrap.Variable()
        self.v_enable = ttkbootstrap.BooleanVar()

        self.entry_name = ttkbootstrap.Entry(self.frame, textvariable=self.v_name, width=20)
        self.entry_type = ttkbootstrap.Combobox(self.frame, values=["tcp", "udp"], textvariable=self.v_type, width=10)
        self.entry_local_ip = ttkbootstrap.Entry(self.frame, textvariable=self.v_local_ip, width=16)
        self.entry_local_port = ttkbootstrap.Spinbox(self.frame, textvariable=self.v_local_port, from_=0, to=65535, width=8)
        self.entry_remote_port = ttkbootstrap.Spinbox(self.frame, textvariable=self.v_remote_port, from_=0, to=65535, width=8)
        self.check_enable = ttkbootstrap.Checkbutton(self.frame, variable=self.v_enable, text=i18n.UI.proxies_c_enable, bootstyle=(OUTLINE, TOOLBUTTON, SUCCESS))
        self.button_delete = ttkbootstrap.Button(self.frame, text=i18n.UI.proxies_c_delete, bootstyle=(DANGER, OUTLINE), command=self.bin_delete)

        self.entry_name.grid(row=self.serial, column=0, sticky=EW, padx=2, pady=2)
        self.entry_type.grid(row=self.serial, column=1, sticky=EW, padx=2, pady=2)
        self.entry_local_ip.grid(row=self.serial, column=2, sticky=EW, padx=2, pady=2)
        self.entry_local_port.grid(row=self.serial, column=3, sticky=EW, padx=2, pady=2)
        self.entry_remote_port.grid(row=self.serial, column=4, sticky=EW, padx=2, pady=2)
        self.check_enable.grid(row=self.serial, column=5, sticky=EW, padx=2, pady=2)
        self.button_delete.grid(row=self.serial, column=6, sticky=EW, padx=2, pady=2)

        self.v_name.trace_add("write", self.bin_name_change)
        self.v_type.trace_add("write", self.bin_type_change)
        self.v_local_ip.trace_add("write", self.bin_local_ip_change)
        self.v_local_port.trace_add("write", self.bin_local_port_change)
        self.v_remote_port.trace_add("write", self.bin_remote_port_change)
        self.v_enable.trace_add("write", self.bin_enable_change)

        self.v_name.set("")
        self.v_type.set("tcp")
        self.v_local_ip.set("127.0.0.1")
        self.v_local_port.set(0)
        self.v_remote_port.set(0)
        self.v_enable.set(True)

    def bin_name_change(self, *_) -> None:
        name = self.v_name.get()

        if not name:
            self.entry_name.configure(bootstyle=(DANGER))
            self.__validity[0] = False
            return

        names = self.master.get_all_proxy_names()
        names.remove(name)

        if name in names:
            self.entry_name.configure(bootstyle=(WARNING))
            self.__validity[0] = False
            return

        self.entry_name.configure(bootstyle=(DEFAULT))
        self.__validity[0] = True

    def bin_type_change(self, *_) -> None:
        value = self.v_type.get()
        if value in ["tcp", "udp"]:
            self.entry_type.configure(bootstyle=(DEFAULT))
            self.__validity[1] = True

        elif value in ["http", "https", "tcpmux", "stcp", "sudp", "xtcp"]:
            self.entry_type.configure(bootstyle=(WARNING))
            self.__validity[1] = False

        else:
            self.entry_type.configure(bootstyle=(DANGER))
            self.__validity[1] = False

    def bin_local_ip_change(self, *_) -> None:
        if self.v_local_ip.get():
            self.entry_local_ip.configure(bootstyle=(DEFAULT))
            self.__validity[2] = True

        else:
            self.entry_local_ip.configure(bootstyle=(DANGER))
            self.__validity[2] = False

    def bin_local_port_change(self, *_) -> None:
        value = self.v_local_port.get()
        try:
            value = int(value)
            if 0 <= value <= 65535:
                self.entry_local_port.configure(bootstyle=(DEFAULT))
                self.__validity[3] = True

            else:
                self.entry_local_port.configure(bootstyle=(DANGER))
                self.__validity[3] = False

        except ValueError:
            self.entry_local_port.configure(bootstyle=(DANGER))
            self.__validity[3] = False

    def bin_remote_port_change(self, *_) -> None:
        value = self.v_remote_port.get()
        try:
            value = int(value)
            if 0 <= value <= 65535:
                self.entry_remote_port.configure(bootstyle=(DEFAULT))
                self.__validity[4] = True

            else:
                self.entry_remote_port.configure(bootstyle=(DANGER))
                self.__validity[4] = False

        except ValueError:
            self.entry_remote_port.configure(bootstyle=(DANGER))
            self.__validity[4] = False

    def bin_enable_change(self, *_) -> None:
        if self.v_enable.get():
            self.check_enable.configure(text=i18n.UI.proxies_c_enable, bootstyle=(OUTLINE, TOOLBUTTON, SUCCESS))

        else:
            self.check_enable.configure(text=i18n.UI.proxies_c_disable, bootstyle=(OUTLINE, TOOLBUTTON, WARNING))

    def bin_delete(self, *_) -> None:
        self.master.bin_delete_proxy(self)

    def forget(self) -> None:
        self.entry_name.grid_forget()
        self.entry_type.grid_forget()
        self.entry_local_ip.grid_forget()
        self.entry_local_port.grid_forget()
        self.entry_remote_port.grid_forget()
        self.check_enable.grid_forget()
        self.button_delete.grid_forget()
