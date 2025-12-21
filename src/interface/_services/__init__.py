# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

__all__ = ["Services"]

# site
import ttkbootstrap

from typex import Singleton, once
from ttkbootstrap.constants import *

# local
import core
import constants
import interface

# internal
from . import _minutiae
from . import _enumerate


class Services (Singleton):
    def __init__(self) -> None:
        self.frame = ttkbootstrap.Frame(interface.mainwindow)
        self.build()

    @once
    def build(self) -> None:
        self.frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.frame_enumerate = ttkbootstrap.Frame(self.frame)
        self.frame_minutiae = ttkbootstrap.Frame(self.frame)
        self.frame_enumerate.pack(side=LEFT, fill=Y)
        self.frame_minutiae.pack(side=RIGHT, fill=BOTH, expand=True, padx=(5, 0))
        self.enumerate = _enumerate.Enumerate(self)
        self.minutiae = _minutiae.Minutiae(self)


def initialize_final() -> None:
    services = Services()
    core.event.subscribe(constants.event.MAINLOOP, services.enumerate.update)
