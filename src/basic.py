# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

__all__ = ["abscwd", "cwd", "i18n"]

# site
from typex import Directory, FilePath
from i18nco import Internationalization, I18nString


class _CWD (Directory):
    class assets (Directory):
        i18n = "i18n"
        favicon = FilePath("favicon.ico")
        frpc = FilePath("frpc.exe")

    instances = "instances"


class _LocalI18n (Internationalization):
    slogan: I18nString

    class UI (object):
        create: I18nString
        rename: I18nString
        remove: I18nString


abscwd = _CWD()
_CWD._include_ = False
cwd = _CWD()

i18n = _LocalI18n()
