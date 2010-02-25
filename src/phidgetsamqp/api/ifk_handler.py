"""
    AMQP API
    
    @author: jldupont

    Created on 2010-02-15
"""
__all__=[]

import dbus.service

from system.mbus import Bus

def deviceHelper(device):
    dev={}
    for key in device:
        dev[str(key)]=str(device[key])
    return dev
            

class DBusAPIHandler(dbus.service.Object):
    """
    DBus signals handler
    """
    PATH="/Device"
    
    def __init__(self):
        self.bus=dbus.SessionBus()
        bus_name = dbus.service.BusName("com.phidgets.Ifk", bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, self.PATH)
        self.bus.add_signal_receiver(self.Devices, "Devices", "com.phidgets.Phidgets", None, "/Device")
        
    ## ============================================================================
    ## SIGNAL HANDLERS  (receiving)
    ## ============================================================================     
    
    def Devices(self, devices):
        """ Signal Handler
        
            Signal normally issued by Phidgets-Manager
        """
        for device in devices:
            ddetails=deviceHelper(device)
            Bus.publish(self, "%device", ddetails)
            
    """
    dbus.Array([dbus.Dictionary({dbus.String(u'serial'): dbus.Int32(80860, variant_level=1), 
    dbus.String(u'version'): dbus.Int32(605, variant_level=1), 
    dbus.String(u'type'): dbus.String(u'PhidgetInterfaceKit', variant_level=1), 
    dbus.String(u'name'): dbus.String(u'Phidget InterfaceKit 0/16/16', variant_level=1)}, 
    signature=dbus.Signature('sv'))], signature=dbus.Signature('a{sv}'))
    """
    """ dbus.Array:
    ['__class__', '__cmp__', '__contains__', '__delattr__', '__delitem__', '__doc__', '__eq__', 
    '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', 
    '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', 
    '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 
    'copy', 'fromkeys', 'get', 'has_key', 'items', 'iteritems', 'iterkeys', 'itervalues', 
    'keys', 'pop', 'popitem', 'setdefault', 'signature', 'update', 'values', 'variant_level']
    """

    ## ============================================================================
    ## SIGNAL GENERATORS
    ## ============================================================================
    

    @dbus.service.signal(dbus_interface="com.phidgets.Phidgets", signature="a{sv}")
    def Error(self, dic):
        """Generated when an error on a device is detected"""

    @dbus.service.signal(dbus_interface="com.phidgets.Phidgets", signature="sii")
    def Din(self, serial, pin, value):
        """Generated when the state of a digital input changes"""

    @dbus.service.signal(dbus_interface="com.phidgets.Phidgets", signature="sii")
    def Dout(self, serial, pin, value):
        """Generated when the state of a digital output changes"""

    @dbus.service.signal(dbus_interface="com.phidgets.Phidgets", signature="sii")
    def Ain(self, serial, pin, value):
        """Generated when the state of an analog input changes"""


    

_handler=DBusAPIHandler()
Bus.subscribe("%device-error",    _handler.Error)
Bus.subscribe("%device-din",      _handler.Din)
Bus.subscribe("%device-dout",     _handler.Dout)
Bus.subscribe("%device-ain",      _handler.Ain)
