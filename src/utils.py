# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

from types import ModuleType


def exec_initialize_activitys(activitys: list[ModuleType], stage: int) -> None:
    """
    执行模块的初始化函数
    """
    name_map = ["initialize_first", "initialize_setup", "initialize_final"]
    attribute_name = name_map[stage]

    for activity in activitys:
        objective = getattr(activity, attribute_name, None)
        objective() if callable(objective) else None
