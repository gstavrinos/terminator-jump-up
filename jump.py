import os
import gtk
import signal
from socket import gethostname
from getpass import getuser
import terminatorlib.plugin as plugin
from terminatorlib.util import err, dbg
from terminatorlib.translation import _
from terminatorlib.terminator import Terminator

# AVAILABLE must contain a list of all the classes that you want exposed
AVAILABLE = ['JumpUp']

class JumpUp(plugin.MenuItem):
    capabilities = ['terminal_menu']

    def __init__(self):
        plugin.MenuItem.__init__(self)
        self.entry = Terminator().windows[0]
        self.entry.connect('key-release-event', self.onKeyPress)
        

    def callback(self, menuitems, menu, terminal):
        item = gtk.MenuItem(_('JumpUp!'))
        item.connect("activate", self.jumpUp)
        menuitems.append(item)

    def jumpUp(self, widget):
        try:
            #t = Terminator().get_focussed_terminal().get_vte()
            t = Terminator().terminals[0].get_vte()
            dbg('\033[1;31mJumpUp row: %s\033[0m' % t.scrollbar_position())
            col, row = t.get_cursor_position()
            content = t.get_text_range(0, 0, row, col, lambda *a: True).split("\n")[:-1]
            dbg('\033[1;31mJumpUp content: %s\033[0m' % content)
            dbg('\033[1;31mJumpUp col: %s\033[0m' % col)
            dbg('\033[1;31mJumpUp row: %s\033[0m' % row)
            #t.set_cursor_position(col, 0)
            #https://stackoverflow.com/questions/11353184/gtk-programmatically-scroll-back-a-single-line-in-scrolled-window-containing-a
        except Exception, ex:
            dbg('\033[1;31mJumpUp failed: %s\033[0m' % ex)

    def onKeyPress(self, widget, event):
        dbg('\033[1;31mJumpUp user: %s\033[0m' % getuser())
        dbg('\033[1;31mJumpUp hostname: %s\033[0m' % gethostname())
        if (event.state & gtk.gdk.MOD1_MASK == gtk.gdk.MOD1_MASK) and (event.keyval == 74 or event.keyval == 106): # Alt+J or Alt+j
            self.jumpUp(widget)
