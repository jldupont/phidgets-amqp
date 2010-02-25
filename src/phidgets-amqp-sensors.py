#!/usr/bin/env python
"""
    @author: Jean-Lou Dupont
"""
import os
import sys
import gtk

## For development environment
ppkg=os.path.abspath( os.getcwd() +"/phidgetsdbus")
if os.path.exists(ppkg):
    sys.path.insert(0, ppkg)

from system import *
Bus.publish(None, "%logpath", "phidgets-amqp-sensors", "~/.phidgets-amqp/sensors.log")

import dbus.glib
import gobject              #@UnresolvedImport

gobject.threads_init()
dbus.glib.init_threads()

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)
     
from apps import app_sensors
     
#Bus.debug=True

import phidgetsamqp.api.sensors_handler    #@UnusedImport
import phidget.config
import phidget.sensors

def hQuit(*pa):
    gtk.main_quit()

Bus.subscribe("%quit", hQuit)

def idle():
    Bus.publish("__idle__", "%poll")
    return True

gobject.timeout_add(1000, idle)
gtk.main()
