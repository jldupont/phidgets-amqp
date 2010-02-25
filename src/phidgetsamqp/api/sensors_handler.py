"""
    Sensors - AMQP interface
    
    @author: jldupont

    Created on 2010-02-24
"""
__all__=[]

import dbus.service

from system.mbus import Bus

class DBus_Inputs(object):

    def __init__(self):
        self.bus=dbus.SessionBus()
        self.bus.add_signal_receiver(self._hDin,  "Din", "com.phidgets.Phidgets", None, "/Device")
        self.bus.add_signal_receiver(self._hDout, "Dout", "com.phidgets.Phidgets", None, "/Device")
        self.bus.add_signal_receiver(self._hAin,  "Ain", "com.phidgets.Phidgets", None, "/Device")

    def _hDin(self, serial, pin, value):
        Bus.publish(self, "%din", serial, pin, value)
    
    def _hDout(self, serial, pin, value):
        Bus.publish(self, "%dout", serial, pin, value)

    def _hAin(self, serial, pin, value):
        Bus.publish(self, "%ain", serial, pin, value)

_ins=DBus_Inputs()


class DBus_State(dbus.service.Object):
    """
    DBus signals handler
    """
    PATH    = "/State"
    BUS_NAME= "org.sensors"
    INTERF  = "org.sensors"
    
    def __init__(self):
        self.bus=dbus.SessionBus()
        bus_name = dbus.service.BusName(self.BUS_NAME, self.bus)
        dbus.service.Object.__init__(self, bus_name, self.PATH)
        
    @dbus.service.signal(dbus_interface="org.sensors", signature="ssv")
    def State(self, device_id, sensor_name, sensor_state):
        """Generated when a sensor changes state"""
    

_shandler=DBus_State()
Bus.subscribe("%state-changed", _shandler.State)


class DBus_Config(dbus.service.Object):
    """
    DBus signals handler
    """
    PATH    = "/Config"
    BUS_NAME= "org.sensors"
    INTERF  = "org.sensors"
    
    def __init__(self):
        bus_name = dbus.service.BusName(self.BUS_NAME, bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, self.PATH)
        
    @dbus.service.signal(dbus_interface="org.sensors", signature="a{sv}")
    def Sensors(self, config):
        """Generated when sensor configuration changess and
            also periodically
        """
    

_chandler=DBus_Config()
Bus.subscribe("%config-sensors", _chandler.Sensors)

