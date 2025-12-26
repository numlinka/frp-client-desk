# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

# std
import threading

# site
from PIL import Image
from typex import Singleton, once
from pystray import Icon, MenuItem

# local
import env
import core
import module
import interface
from basic import cwd, i18n


class Tray (Singleton):
    def __init__(self):
        self.icon = Image.open(cwd.assets.favicon)

    def bin_deiconify(self, _: MenuItem):
        interface.mainwindow.deiconify()

    def bin_stop_all_instances(self, _: MenuItem):
        for name in module.services.instances_names():
            module.services.instance(name).stop()

    def bin_exit(self, _: MenuItem):
        core.actions.exit.run()

    def run(self):
        menu = (
            MenuItem(i18n.tray.deiconify, self.bin_deiconify, default=True, visible=False),
            MenuItem(i18n.tray.deiconify, self.bin_deiconify),
            MenuItem(i18n.tray.stop_all_instances, self.bin_stop_all_instances),
            MenuItem(i18n.tray.exit, self.bin_exit)
        )
        icon = Icon(env.name, self.icon, i18n.tray.name, menu)
        icon.run()

    @once
    def start(self):
        threading.Thread(target=self.run, name="SystemTray", args=(), daemon=True).start()


@once
def initialize_final() -> None:
    tray = Tray()
    tray.start()
