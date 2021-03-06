"""
    Ifk Manager
    
    - snoops on exchange "org.phidgets" / "device.devices"
      for "type=PhidgetInterfaceKit"
    
    @author: jldupont

    Created on 2010-02-28
"""
__all__=[]

from time import sleep
import json
from Queue import Queue, Empty
from threading import Thread
from amqplib import client_0_8 as amqp #@UnresolvedImport

from system.mbus import Bus

### Communications queues
### ---------------------
qToManagerConsumer=Queue()
qFromManagerConsumer=Queue()


class ManagerMessagesConsumer(Thread):
    """
    Manages the reception of "device.devices" message
    from the AMQP fabric
    
    @param iq: input to the thread
    @param oq: output from the thread
    """
    EXCH="org.phidgets"
    RKEY="device.devices"
    RQU="q.device.devices"
    
    TIMEOUT=0.100
    
    def __init__(self, iq, oq):
        Thread.__init__(self)
        self.iq=iq
        self.oq=oq
        self.config=None
        self.conn=None
        self.chan=None
        
    def run(self):
        """ entry point 
        """
        while True:
            mtype, mdata=self.gMsg()
            if mtype=="quit":
                break
            if mtype=="config-amqp":
                self.closeConn()
                self.config=mdata
                self.connect()
            if mtype is not None:
                continue  ## empty the queue... paranoia
            
            if self.conn:
                try:     self.chan.wait()
                except:  self.closeConn()
            sleep(self.TIMEOUT)
            
        
    def gMsg(self):
        try:          msg=self.iq.get_nowait()
        except Empty: msg=(None, None) 
        return msg

    def amqpCallback(self, msg):
        """ Callback from AMQP """
        self.oq.put(("msg", msg.body))

    def connect(self):
        """ Perform connection to AMQP broker """
        try:
            self.conn = amqp.Connection(insist=True, **self.config)
            self.chan = self.conn.channel()
            self.chan.queue_declare(queue=self.RQU, durable=False, exclusive=False, auto_delete=True)
            self.chan.exchange_declare(exchange=self.EXCH, type="topic", durable=True, auto_delete=False,)
            self.chan.queue_bind(queue=self.RQU, exchange=self.EXCH, routing_key=self.RKEY)
            self.chan.basic_consume(queue=self.RQU, no_ack=True, callback=self.amqpCallback, consumer_tag="ctag")
        except:
            self.closeConn()
            
    def closeConn(self):
        try:    self.chan.basic_cancel("ctag")
        except: pass
        try:    self.chan.close()
        except: pass
        try:    self.conn.close()
        except: pass
        self.chan=None
        self.conn=None

        
                
_mmc=ManagerMessagesConsumer(qToManagerConsumer, qFromManagerConsumer)
_mmc.start()



class IfkManagerAgent(object):
    """
    """
    LCONFIG = { "%json-decode": 4*60*60
            }

    def __init__(self, qToMMC, qFromMMC):
        self.iq=qFromMMC
        self.oq=qToMMC
        Bus.publish(self,"%llconfig", self.LCONFIG)
        
    def _hConfigAmqp(self, config):
        self.oq.put(("config-amqp", config))
        
    def _hquit(self):
        self.oq.put(("quit", None))
        
    def _hpoll(self, pc):
        """ Publishes any messages queued
            to the local Bus
        """
        while True:
            mtype, mdata=self.gMsg()
            if mtype=="msg":
                self.processMsg(mdata)
                continue
            if mtype is None:
                break
        
    def gMsg(self):
        try:          msg=self.iq.get_nowait()
        except Empty: msg=(None, None) 
        return msg

    def processMsg(self, data):
        
        try:   
            devices=json.loads(data)
        except Exception,e:
            Bus.publish(self, "%llog", "%json-decode", 
                        "warning", "Error(%s) decoding json object: %s" % (e, data))
            return
    
        ## We need to itemize the devices list
        ##  for the benefit of the other agents sitting on the Bus
        try:
            for device in devices:
                Bus.publish(self, "%device", device)
        except Exception, e:
            Bus.publish(self, "%llog", "%json-decode", 
                        "warning", "Error(%s) accessing json list object: %s" % (e, devices))


_ifkm=IfkManagerAgent(qToManagerConsumer, qFromManagerConsumer)
Bus.subscribe("%config-amqp", _ifkm._hConfigAmqp)
Bus.subscribe("%poll",        _ifkm._hpoll)
Bus.subscribe("%quit",        _ifkm._hquit)
