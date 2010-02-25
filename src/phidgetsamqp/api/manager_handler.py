"""
    AMQP API
    
    @author: jldupont

    Created on 2010-02-15
"""
__all__=[]

import dbus.service

from system.mbus import Bus

class DBusAPIHandler(dbus.service.Object):
    """
    DBus signals handler
    """
    PATH="/Device"
    
    def __init__(self):
        bus_name = dbus.service.BusName('com.phidgets.Manager', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, self.PATH)
        
    @dbus.service.method('com.phidgets.Phidgets', in_signature="s")
    def EchoString(self, original):
        return original

    @dbus.service.signal(dbus_interface="com.phidgets.Phidgets", signature="aa{sv}")
    def Devices(self, liste):
        """Generated when a device is attached to the host"""
    
    @dbus.service.signal(dbus_interface="com.phidgets.Phidgets", signature="a{sv}")
    def Attached(self, dic):
        """Generated when a device is attached to the host"""

    @dbus.service.signal(dbus_interface="com.phidgets.Phidgets", signature="a{sv}")
    def Detached(self, dic):
        """Generated when a device is detached to the host"""

    @dbus.service.signal(dbus_interface="com.phidgets.Phidgets", signature="a{sv}")
    def Error(self, dic):
        """Generated when an error on a device is detected"""


    

_handler=DBusAPIHandler()
Bus.subscribe("%devices",         _handler.Devices)
Bus.subscribe("%device-attached", _handler.Attached)
Bus.subscribe("%device-detached", _handler.Detached)
Bus.subscribe("%device-error",    _handler.Error)


