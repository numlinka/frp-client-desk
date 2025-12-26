# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

__all__ = ["event", "actions"]

# std
import signal

# site
import ezudesign
from typex import once

# local
import tray
import utils
import module
import constants
import interface
from basic import cwd, i18n

# internal
from . import actions


_activitys = [module, interface, tray]

event: ezudesign.eventhub.EventHub


@once
def initialize_first() -> None:
    global event
    event = ezudesign.eventhub.EventHub(constants.event.__all_events__)
    i18n.ctrl.auto_load(cwd.assets.i18n)
    i18n.ctrl.set_locale()

    utils.exec_initialize_activitys(_activitys, 0)


@once
def initialize_setup() -> None:
    utils.exec_initialize_activitys(_activitys, 1)


@once
def initialize_final() -> None:
    signal.signal(signal.SIGINT, actions.exit.run)
    signal.signal(signal.SIGTERM, actions.exit.run)
    utils.exec_initialize_activitys(_activitys, 2)


@once
def initialize() -> None:
    initialize_first()
    initialize_setup()
    initialize_final()


@once
def run() -> None:
    initialize()
    interface.mainwindow.mainloop()
