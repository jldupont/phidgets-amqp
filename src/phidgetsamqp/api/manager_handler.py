"""
    AMQP API
    
    @author: jldupont

    Created on 2010-02-15
"""
__all__=[]
import json

from amqplib import client_0_8 as amqp #@UnresolvedImport


from system.mbus import Bus

class DBusAPIHandler(object):
    """
    DBus signals handler
    """
    PATH="/Device"
    
    LCONFIG = {"%conn-error" : 4*60*60 
                }
    
    DEFAULT_CONN_RETRY = 4
    EXCH="org.phidgets"
    
    def __init__(self):
        self.config=None
        self.conn=None
        self.chan=None
        self.cpoll=0
        self.cLastConnAttempt=0
        Bus.publish(self,"%llconfig", self.LCONFIG)
        

    def Devices(self, liste):
        """Generated when a device is attached to the host"""
        self.sMsg("device.devices", liste)

    def Attached(self, dic):
        """Generated when a device is attached to the host"""
        self.sMsg("device.attached", dic)

    def Detached(self, dic):
        """Generated when a device is detached to the host"""
        self.sMsg("device.detached", dic)

    def Error(self, dic):
        """Generated when an error on a device is detected"""
        self.sMsg("device.error", dic)

    def sMsg(self, rkey, msg):
        try:    jmsg=json.dumps(msg)
        except:
            self.log("%json-encode", "warning", "Devices: error encoding to JSON: %s" % msg)
            return        
        msg = amqp.Message(jmsg)
        msg.properties["delivery_mode"] = 1
        msg.content_type="application/json"
        self.chan.basic_publish(msg,exchange=self.EXCH, routing_key=rkey)        

    def _hconfig(self, config):
        """ Configuration Changed handler """
        self.config=config
        
    def _hpoll(self, pc):
        """ Polling Event handler
        
            If a connection is active, try
            making one provided that we do not
            exceed a certain retry rate
        """
        self.cpoll=pc
        if not self.conn:
            delta=self.cpoll - self.cLastConnAttempt
            self.cLastConnAttempt = pc
            if delta >= self.DEFAULT_CONN_RETRY:
                self.setup()
        
    ## ======================================================
        
    def setup(self):
        """ Setup the connection & channel """
        try:
            self.conn=amqp.Connection(insist=False, **self.config)
        except Exception,e:
            self.conn=None
            Bus.publish(self, "%conn-error")
            self.log("%conn-error", "error", 
                     "Failed to connect to AMQP broker. Exception(%s)" % e)
            return
        
        try:
            self.chan=self.conn.channel()
        except Exception,e:
            self.chan=None
            try:    self.conn.close()
            except: pass
            Bus.publish(self, "%conn-error")
            self.log("%conn-error", "error", 
                    "Failed to acquire channel on connection to AMQP broker. Exception(%s)" % e)
            
            self.log("%conn-open", "info", "Connection to AMQP broker opened")
            
    def log(self, ltype, level, msg):
        Bus.publish(self, "%llog", ltype, level, msg)

    

_handler=DBusAPIHandler()
Bus.subscribe("%devices",         _handler.Devices)
Bus.subscribe("%device-attached", _handler.Attached)
Bus.subscribe("%device-detached", _handler.Detached)
Bus.subscribe("%device-error",    _handler.Error)

Bus.subscribe("%config-amqp",     _handler._hconfig)
Bus.subscribe("%poll",            _handler._hpoll)
