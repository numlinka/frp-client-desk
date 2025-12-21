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
        minutiae_null: I18nString
        common: I18nString
        link: I18nString
        open_in_browser: I18nString
        options: I18nString
        option_run: I18nString
        option_stop: I18nString
        option_reload: I18nString
        option_save: I18nString
        option_value_err: I18nString
        option_common_err: I18nString
        option_proxie_err: I18nString
        proxies: I18nString
        proxies_name: I18nString
        proxies_type: I18nString
        proxies_local_ip: I18nString
        proxies_local_port: I18nString
        proxies_remote_port: I18nString
        proxies_enable: I18nString
        proxies_delete: I18nString
        proxies_add: I18nString
        proxies_del_err: I18nString
        proxies_del_err_t: I18nString
        proxies_c_enable: I18nString
        proxies_c_disable: I18nString
        proxies_c_delete: I18nString
        terminal: I18nString
        enum_new_ins: I18nString
        enum_new_ins_t: I18nString
        enum_new_ins_err: I18nString
        enum_new_ins_err_t_null: I18nString
        enum_new_ins_err_t_exist: I18nString
        enum_new_ins_err_t_valid: I18nString
        enum_del_ins: I18nString
        enum_del_ins_t: I18nString
        enum_del_ins_err: I18nString
        enum_del_ins_err_t: I18nString
        enum_c_running: I18nString
        enum_c_delete: I18nString
        enum_c_create: I18nString


abscwd = _CWD()
_CWD._include_ = False
cwd = _CWD()

i18n = _LocalI18n()
