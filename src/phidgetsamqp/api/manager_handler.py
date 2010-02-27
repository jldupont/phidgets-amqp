"""
    AMQP API
    
    @author: jldupont

    Created on 2010-02-15
"""
__all__=[]

from amqplib import client_0_8 as amqp #@UnresolvedImport


from system.mbus import Bus

class DBusAPIHandler(object):
    """
    DBus signals handler
    """
    PATH="/Device"
    
    LOG_RATE = {"%conn-error" : 4*60*60 
                }
    
    def __init__(self):
        self.config=None
        self.conn=None
        self.chan=None
        

    def Devices(self, liste):
        """Generated when a device is attached to the host"""
    

    def Attached(self, dic):
        """Generated when a device is attached to the host"""

    def Detached(self, dic):
        """Generated when a device is detached to the host"""

    def Error(self, dic):
        """Generated when an error on a device is detected"""

    def _hconfig(self, config):
        """ Configuration Changed handler """
        self.config=config
        
    def _hpoll(self, *_p):
        """ Polling Event handler """
        
    ## ======================================================
        
    def setup(self):
        """ Setup the connection & channel """
        try:
            self.conn=amqp.Connection(insist=False, **self.config)
        except Exception,e:
            self.conn=None
            Bus.publish(self, "%conn-error")
            self.maybeLog("%conn-error", "error", 
                          "Failed to connect to AMQP broker. Exception(%s)" % e)
            return
        
        try:
            self.chan=self.conn.channel()
        except Exception,e:
            self.chan=None
            try:    self.conn.close()
            except: pass
            Bus.publish(self, "%conn-error")
            self.maybeLog("%conn-error", "error", 
                          "Failed to acquire channel on connection to AMQP broker. Exception(%s)" % e)
            
            
    def maybeLog(self, etype, level, msg):
        pass
    

_handler=DBusAPIHandler()
Bus.subscribe("%devices",         _handler.Devices)
Bus.subscribe("%device-attached", _handler.Attached)
Bus.subscribe("%device-detached", _handler.Detached)
Bus.subscribe("%device-error",    _handler.Error)

Bus.subscribe("%config-amqp",     _handler._hconfig)
Bus.subscribe("%poll",            _handler._hpoll)