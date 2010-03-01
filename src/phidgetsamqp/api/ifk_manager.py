"""
    Ifk Manager
    
    - snoops on exchange "org.phidgets" / "device.devices"
      for "type=PhidgetInterfaceKit"
    
    @author: jldupont

    Created on 2010-02-28
"""
__all__=[]

import json
from Queue import Queue, Empty, Full
from amqplib import client_0_8 as amqp #@UnresolvedImport

from system.mbus import Bus

class ManagerMessagesConsumer(object):
    def __init__(self):
        pass
    



class IfkManagerAgent(object):
    
    def __init__(self):
        self.iq=Queue()
        self.oq=Queue()
        
    def _hConfigAmqp(self, config):
        self.iq.put(("config-amqp", config))
        
    def _hpoll(self, pc):
        """ Publishes any messages queued
            to the local Bus
        """
        while True:
            try:          msg=self.oq.get_nowait()
            except Empty: msg=None
            if msg is None:
                break

            _mtype=msg.pop(0)            
            Bus.publish(self, _mtype, *msg)        

        
    
_ifkm=IfkManagerAgent()
Bus.subscribe("%config-amqp", _ifkm._hConfigAmqp)
Bus.subscribe("%poll",        _ifkm._hpoll)