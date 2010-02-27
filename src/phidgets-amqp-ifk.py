#!/usr/bin/env python
"""
    @author: Jean-Lou Dupont
"""
import os
import sys
import gtk

## For development environment
ppkg=os.path.abspath( os.getcwd() +"/phidgetsamqp")
if os.path.exists(ppkg):
    sys.path.insert(0, ppkg)

from system import *
Bus.publish(None, "%logpath", "phidgets-amqp-ifk", "~/.phidgets-amqp/ifk.log")

import dbus.glib
import gobject              #@UnresolvedImport

gobject.threads_init()
dbus.glib.init_threads()

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)
     
from apps import app_ifk
     
#Bus.debug=True

import phidgetsamqp.api.config
import phidgetsamqp.api.ifk_handler    #@UnusedImport
import phidget.ifk

def hQuit(*pa):
    gtk.main_quit()

Bus.subscribe("%quit", hQuit)

def idle():
    Bus.publish("__idle__", "%poll")
    return True

gobject.timeout_add(250, idle)
gtk.main()
