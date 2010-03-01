"""
    AMQP API
    
    @author: jldupont

    Created on 2010-02-15
"""
__all__=[]

from system.mbus import Bus
from system.amqp import AMQPCommTx  #@UnresolvedImport


class IfkAmqpAgent(object):
    """ Interface to AMQP
    """
    EXCH="org.phidgets"
    
    LCONFIG = {"%conn-open": 0
               ,"%conn-error" :  4*60 
               ,"%json-encode": 4*60*60
                }  
    
    def __init__(self):
        self.config=None
        self.comm=None
        Bus.publish(self, "%llconfig", self.LCONFIG)
    
    def _hconfig(self, config):
        self.config=config
    
    def Error(self, dic):
        """Generated when an error on a device is detected"""
        if self.comm:
            self.comm.publish("device.error", dic)

    def Din(self, serial, pin, value):
        """Generated when the state of a digital input changes"""
        if self.comm:
            self.comm.publish("device.io.din", {"serial": serial, "pin":pin, "value": value})

    def Dout(self, serial, pin, value):
        """Generated when the state of a digital output changes"""
        if self.comm:
            self.comm.publish("device.io.dout", {"serial": serial, "pin":pin, "value": value})

    def Ain(self, serial, pin, value):
        """Generated when the state of an analog input changes"""
        if self.comm:
            self.comm.publish("device.io.ain", {"serial": serial, "pin":pin, "value": value})
        

    def _hpoll(self, pc):
        if self.config is None:
            Bus.publish(self, "%config-amqp?")

        if self.comm is not None:
            if not self.comm.isOk():
                del self.comm
                self.comm=None
            
        if self.comm is None:
            self.comm=AMQPCommTx(self.config, self.EXCH)
            self.comm.connect()

            

    
_handler=IfkAmqpAgent()
Bus.subscribe("%device-error",    _handler.Error)
Bus.subscribe("%device-din",      _handler.Din)
Bus.subscribe("%device-dout",     _handler.Dout)
Bus.subscribe("%device-ain",      _handler.Ain)

Bus.subscribe("%poll",            _handler._hpoll)
Bus.subscribe("%config-amqp",     _handler._hconfig)

