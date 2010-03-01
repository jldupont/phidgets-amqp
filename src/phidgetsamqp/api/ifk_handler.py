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
            

class IfkAmqpAgent(object):
    """ Interface to AMQP
    """
    def __init__(self):
        pass
    
    def Error(self, dic):
        """Generated when an error on a device is detected"""

    def Din(self, serial, pin, value):
        """Generated when the state of a digital input changes"""

    def Dout(self, serial, pin, value):
        """Generated when the state of a digital output changes"""

    def Ain(self, serial, pin, value):
        """Generated when the state of an analog input changes"""

    
_handler=IfkAmqpAgent()
Bus.subscribe("%device-error",    _handler.Error)
Bus.subscribe("%device-din",      _handler.Din)
Bus.subscribe("%device-dout",     _handler.Dout)
Bus.subscribe("%device-ain",      _handler.Ain)

