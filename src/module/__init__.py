# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

# site
from typex import once

# local
import utils

# internal
from . import _services


_activitys = [_services]

services: _services.Services


@once
def initialize_first() -> None:
    utils.exec_initialize_activitys(_activitys, 0)


@once
def initialize_setup() -> None:
    utils.exec_initialize_activitys(_activitys, 1)


@once
def initialize_final() -> None:
    utils.exec_initialize_activitys(_activitys, 2)
