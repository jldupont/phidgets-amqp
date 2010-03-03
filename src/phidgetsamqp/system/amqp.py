"""
    @author: jldupont

    Created on 2010-03-01
"""
__all__=["AMQPCommRx", "AMQPCommTx"]

import json
from Queue import Queue, Empty
from amqplib import client_0_8 as amqp #@UnresolvedImport

from system.mbus import Bus

class AMQPComm(object):
    def __init__(self, config, exch):
        self.config=config
        self.conn=None
        self.chan=None
        self.exch=exch
        
    def __del__(self):
        self.closeConn()
        
    def _connect(self):
        """ Perform connection to AMQP broker """
        try:
            self.conn = amqp.Connection(insist=True, **self.config)
            self.chan = self.conn.channel()
            self.chan.exchange_declare(exchange=self.exch, type="topic", durable=True, auto_delete=False,)
            self.log("%conn-open", "info", "Connection to AMQP broker opened")
        except Exception,e:
            self.log("%conn-error", "error", "Error whilst connecting to AMQP broker (%s)" % e)
            self.closeConn()
            
    def closeConn(self):
        try:    self.chan.close()
        except: pass
        try:    self.conn.close()
        except: pass
        self.chan=None
        self.conn=None
        
    def log(self, ltype, level, msg):
        Bus.publish(self, "%llog", ltype, level, msg)
        
    def isOk(self):
        return self.conn is not None

        
    
class AMQPCommTx(AMQPComm):
    def __init__(self, config, exch):
        AMQPComm.__init__(self, config, exch)
        
    def connect(self):
        self._connect()
        
    def publish(self, rkey, msg):
        try:    jmsg=json.dumps(msg)
        except:
            self.log("%json-encode", "Error", "Error encoding to JSON: %s" % msg)
            return        
        msg = amqp.Message(jmsg)
        msg.properties["delivery_mode"] = 2
        msg.content_type="application/json"
        
        if not self.chan:
            Bus.publish(self, "%llog", "%conn-error", "error", "Connection to AMQP broker not opened")
            return
        
        try:
            #print "AMQPCommTx.publish: rkey(%s) msg(%s)" % (rkey, jmsg)
            self.chan.basic_publish(msg, exchange=self.exch, routing_key=rkey)
        except Exception,e:
            #print "sMsg: rkey(%s) jmsg(%s)" % (rkey, jmsg)
            self.log("%conn-error", "error", "Failed to send message to AMQP broker: %s" % e)
            self.closeConn()


class AMQPCommRx(AMQPComm):
    
    def __init__(self, config, exch, rkey=None, rq=None):
        AMQPComm.__init__(config, exch)
        self.oq=Queue()
        self.rkey=rkey
        self.rq=rq
        self.ctag=id(self)
        
    def gMsg(self):
        try:          msg=self.oq.get_nowait()
        except Empty: msg=(None, None) 
        return msg
               
    def _amqpCallback(self, msg):
        """ Callback from AMQP """
        self.oq.put(("msg", msg.body))

    def connect(self):
        """ Perform connection to AMQP broker """
        self._connect()
        if self.conn is not None:
            try:
                self.chan.queue_declare(queue=self.rq, durable=True, exclusive=False, auto_delete=False)
                self.chan.queue_bind(queue=self.rq, exchange=self.exch, routing_key=self.RKEY)
                self.chan.basic_consume(queue=self.rq, no_ack=True, callback=self._amqpCallback, consumer_tag=self.ctag)
            except:
                self.closeConn()
            
