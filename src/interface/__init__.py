# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

# site
import ttkbootstrap

from typex import once
from ezudesign.utils import try_exec, exec_item
from ttkbootstrap.constants import *

# local
import env
import core
import utils
import constants

# internal
from . import _slogan
from . import _services
from . import methods
from . import annotation_toplevel

_activitys = [_services]

mainwindow: ttkbootstrap.Window
style: ttkbootstrap.Style

annotation: annotation_toplevel.AnnotationToplevel
services: _services.Services
slogan: _slogan.Slogan


@once
def initialize_first() -> None:
    global mainwindow, style, annotation
    mainwindow = ttkbootstrap.Window()
    style = ttkbootstrap.Style()

    mainwindow.title(f"{env.name} v{env.version} -by {env.author}")
    # mainwindow.geometry("700x450")
    mainwindow.geometry("950x600")

    annotation = annotation_toplevel.AnnotationToplevel()
    utils.exec_initialize_activitys(_activitys, 0)


@once
def initialize_setup() -> None:
    global services, slogan
    services = _services.Services()
    slogan = _slogan.Slogan()
    utils.exec_initialize_activitys(_activitys, 1)


@once
def initialize_final() -> None:
    mainwindow.after(100, lambda *_: core.event.emit(constants.event.MAINLOOP))
    utils.exec_initialize_activitys(_activitys, 2)
