# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# frp-client-desk Copyright (c) 2025 numlinka.

__all__ = ["Slogan"]

# std
import ttkbootstrap

from ttkbootstrap.constants import *
from typex import once

# local
import env
import interface
from basic import i18n


class Slogan (object):
    def __init__(self):
        self.parent = interface.mainwindow
        self.build()

    @once
    def build(self):
        self.frame = ttkbootstrap.Frame(self.parent)
        self.slogan = ttkbootstrap.Label(self.frame, text=i18n.slogan, cursor="hand2", bootstyle=INFO)
        self.license = ttkbootstrap.Label(self.frame, text=f"{env.license} | {env.name} {env.copyright}", cursor="hand2", bootstyle=INFO)

        self.frame.pack(side=BOTTOM, fill=X, padx=5, pady=(0, 5))
        self.license.pack(side=RIGHT)
        self.slogan.pack(side=LEFT)

        self.slogan.bind("<Button-1>", self.bin_open_url_slogan)
        self.license.bind("<Button-1>", self.bin_open_url_license)

    def bin_open_url_slogan(self, *_):
        import webbrowser
        webbrowser.open("https://afdian.com/a/numlinka")

    def bin_open_url_license(self, *_):
        import webbrowser
        webbrowser.open(env.url)
