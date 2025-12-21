# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

__all__ = []

# std
import tkinter

# site
import ttkbootstrap


def treeview_tag_add(treeview: ttkbootstrap.Treeview, item: str, tag: str) -> bool:
    tags = set(treeview.item(item, "tags"))
    if tag not in tags:
        tags.add(tag)
        treeview.item(item, tags=tuple(tags))
        return True
    return False

def treeview_tag_remove(treeview: ttkbootstrap.Treeview, item: str, tag: str) -> bool:
    tags = set(treeview.item(item, "tags"))
    if tag in tags:
        tags.remove(tag)
        treeview.item(item, tags=tuple(tags))
        return True
    return False

def treeview_value_set(treeview: ttkbootstrap.Treeview, item: str, index: int, value: str) -> None:
    values = list(treeview.item(item, "values"))
    if len(values) <= index:
        values.extend([""] * (index - len(values) + 1))
    values[index] = value
    treeview.item(item, values=tuple(values))

def fake_withdraw(window: tkinter.Wm):
    window.geometry("+32000+32000")
