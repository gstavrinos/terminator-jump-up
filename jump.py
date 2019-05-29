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
            t = Terminator().last_focused_term
            col, row = t.get_vte().get_cursor_position()
            content = t.get_vte().get_text_range(0, 0, row, col, lambda *a: True).split("\n")
            width = t.get_vte().get_column_count()
            last_username = content[-2].split("@")[0]
            last_hostname = content[-2].split("@")[1].split(":")[0]
            content_as_seen = []
            for line in content[:-2]:
                if len(line) > width:
                    new_lines = [line[i:i+width] for i in range(0, len(line), width)]
                    for n in new_lines:
                        content_as_seen.append(n)
                else:
                    content_as_seen.append(line)
            machine_username = getuser()
            machine_hostname = gethostname()
            jumpPos = 0
            # Work even when we are connected on another machine, with different username/hostname
            ssh_check = machine_username != last_username and machine_hostname != last_hostname
            ssh_prefix = last_username + "@" + last_hostname + ":"
            normal_prefix = machine_username + "@" + machine_hostname + ":"
            for i in range(len(content_as_seen)-1, 0, -1):
                if (not (content_as_seen[i].endswith("$ ^C") or content_as_seen[i].endswith("$ ")) and (content_as_seen[i].startswith(normal_prefix) or (ssh_check and content_as_seen[i].startswith(ssh_prefix)))):
                    jumpPos = i
                    break
            t.scrollbar_jump(jumpPos)
        except Exception, ex:
            dbg('\033[1;31mJumpUp failed: %s\033[0m' % ex)

    def onKeyPress(self, widget, event):
        if (event.state & gtk.gdk.MOD1_MASK == gtk.gdk.MOD1_MASK) and (event.keyval == 74 or event.keyval == 106): # Alt+J or Alt+j
            self.jumpUp(widget)
