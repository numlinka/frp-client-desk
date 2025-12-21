# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

MAINLOOP = "mainloop"
INSTANCE_SELECTED = "instance_selected"
INSTANCE_SWITCHED = "instance_switched"
INSTANCE_LOG_UPDATED = "instance_log_updated"

__all_events__ = [v for x, v in globals().items() if not x.startswith("_")]
