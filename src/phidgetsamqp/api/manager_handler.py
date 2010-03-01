"""
    AMQP API
    
    @author: jldupont

    Created on 2010-02-15
"""
__all__=[]
import json

from amqplib import client_0_8 as amqp #@UnresolvedImport


from system.mbus import Bus

class APIHandler(object):
    """
    DBus signals handler
    """
    PATH="/Device"
    
    LCONFIG = {"%conn-open": 0
               ,"%conn-error" :  4*60*60 
               ,"%json-encode": 4*60*60
                }
    
    DEFAULT_CONN_RETRY = 4
    EXCH="org.phidgets"
    
    def __init__(self):
        self.config={}
        self.conn=None
        self.chan=None
        self.cpoll=0
        self.cLastConnAttempt=0
        Bus.publish(self,"%llconfig", self.LCONFIG)
        #self.setup()

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

    def sMsg(self, rkey, rmsg):
        if not self.conn:
            return
        
        try:    jmsg=json.dumps(rmsg)
        except:
            self.log("%json-encode", "Error", "Error encoding to JSON: %s" % rmsg)
            return        
        msg = amqp.Message(jmsg)
        msg.properties["delivery_mode"] = 2
        msg.content_type="application/json"
        
        try:
            #print "... sending, cpoll(%s) rkey(%s)" % (self.cpoll, rkey)
            self.chan.basic_publish(msg, exchange=self.EXCH, routing_key=rkey)
        except Exception,e:
            #print "sMsg: rkey(%s) jmsg(%s)" % (rkey, jmsg)
            self.log("%conn-error", "error", "Failed to send message to AMQP broker: %s" % e)
            try:
                self.chan.close()
                self.conn.close()
            except: pass
            finally:
                self.conn=None
                self.chan=None   

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
            if delta >= self.DEFAULT_CONN_RETRY:
                self.cLastConnAttempt = pc                
                self.setup()
        
    ## ======================================================
        
    def setup(self):
        """ Setup the connection & channel """
        Bus.publish(self, "%config-amqp?")
        
        try:
            self.conn=amqp.Connection(insist=True, **self.config)
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
            return
            
        try:
            self.chan.exchange_declare(exchange=self.EXCH, 
                                       type="topic", durable=True, auto_delete=False,)
        except Exception,e:
            Bus.publish(self, "%conn-error")
            self.log("%conn-error", "error", 
                    "Failed to declare exchange on connection to AMQP broker. Exception(%s)" % e)
            try:
                self.chan.close()
                self.conn.close()
                self.chan=None
                self.conn=None
            except: pass
            return
            
        self.log("%conn-open", "info", "Connection to AMQP broker opened")
            
    def log(self, ltype, level, msg):
        Bus.publish(self, "%llog", ltype, level, msg)

    

_handler=APIHandler()
Bus.subscribe("%devices",         _handler.Devices)
Bus.subscribe("%device-attached", _handler.Attached)
Bus.subscribe("%device-detached", _handler.Detached)
Bus.subscribe("%device-error",    _handler.Error)

Bus.subscribe("%config-amqp",     _handler._hconfig)
Bus.subscribe("%poll",            _handler._hpoll)
