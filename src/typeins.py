# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

# std
from dataclasses import dataclass
from typing import Type


@dataclass
class ConfigOption (object):
    name: str
    type_: Type
    description: str = ""
    required: bool = False
