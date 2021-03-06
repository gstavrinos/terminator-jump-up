import os
import re
import signal
from socket import gethostname
from getpass import getuser
import terminatorlib.plugin as plugin
from terminatorlib.util import err, dbg
from terminatorlib.translation import _
from terminatorlib.version import APP_VERSION
from terminatorlib.terminator import Terminator

if float(APP_VERSION) <= 0.98:
    import gtk as Gtk
else:
    import gi
    from gi.repository import Gtk, Gdk

# AVAILABLE must contain a list of all the classes that you want exposed
AVAILABLE = ['JumpUp']

class JumpUp(plugin.MenuItem):
    capabilities = ['terminal_menu']
    last_cursor_pos = 0

    def __init__(self):
        plugin.MenuItem.__init__(self)
        self.entry = Terminator().windows[0]
        self.entry.connect('key-release-event', self.onKeyRelease)
        self.entry.connect('key-press-event', self.onKeyPress)
        

    def callback(self, menuitems, menu, terminal):
        item = Gtk.MenuItem(_('JumpUp!'))
        item.connect("activate", self.jumpUp)
        menuitems.append(item)

    def jumpUp(self, widget):
        t = Terminator().last_focused_term
        t.scrollbar_jump(self.last_cursor_pos)

    def onKeyRelease(self, widget, event):
        if float(APP_VERSION) <= 0.98:
            if (event.state & Gtk.gdk.MOD1_MASK == Gtk.gdk.MOD1_MASK) and (event.keyval == 74 or event.keyval == 106): # Alt+J or Alt+j
                self.jumpUp(widget)
        else:
            if (event.state & Gdk.ModifierType.MOD1_MASK == Gdk.ModifierType.MOD1_MASK) and (event.keyval == 74 or event.keyval == 106): # Alt+J or Alt+j
                self.jumpUp(widget)

    def onKeyPress(self, widget, event):
        if event.keyval == 65293:
            t = Terminator().last_focused_term
            col, row = t.get_vte().get_cursor_position()
            if float(APP_VERSION) <= 0.98:
                content = t.get_vte().get_text_range(row-3, 0, row, col, lambda *a: True).split("\n")
                if re.match("\w+@\w+", content[-2].split(":")[0]) and not content[-2].endswith("$ "):
                    self.last_cursor_pos = row
            else:
                content = t.get_vte().get_text_range(row-3, 0, row, col, lambda *a: True)[0].split("\n")
                if re.match("\w+@\w+", content[-1].split(":")[0]) and not content[-1].endswith("$ "):
                    self.last_cursor_pos = row
