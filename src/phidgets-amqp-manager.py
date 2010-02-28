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
Bus.publish(None, "%logpath", "phidgets-amqp-manager", "~/.phidgets-amqp/manager.log")

import dbus.glib
import gobject              #@UnresolvedImport

gobject.threads_init()
dbus.glib.init_threads()

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)
     
from apps import app_manager
     
#Bus.debug=True

import phidgetsamqp.api.config          #@UnusedImport
import phidgetsamqp.api.manager_handler #@UnusedImport
import phidget.manager

def hQuit(*pa):
    gtk.main_quit()

Bus.subscribe("%quit", hQuit)

def idle(count=0):
    Bus.publish("__idle__", "%poll", count)
    count=count+1
    return True

gobject.timeout_add(1000, idle)
gtk.main()
