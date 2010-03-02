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
Bus.publish(None, "%logpath", "phidgets-amqp-sensors", "~/.phidgets-amqp/sensors.log")

import dbus.glib
import gobject              #@UnresolvedImport

gobject.threads_init()
dbus.glib.init_threads()

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)
     
from apps import app_sensors
     
#Bus.debug=True

import phidgetsamqp.api.config
import phidgetsamqp.api.sensors_manager    #@UnusedImport
import phidget.sensors

def hQuit(*pa):
    gtk.main_quit()

Bus.subscribe("%quit", hQuit)

pcount=0
def idle():
    global pcount
    Bus.publish("__idle__", "%poll", pcount)
    pcount=pcount+1
    return True

gobject.timeout_add(100, idle)
gtk.main()
