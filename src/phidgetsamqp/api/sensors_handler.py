"""
    Sensors - AMQP interface
    
    @author: jldupont

    Created on 2010-02-24
"""
__all__=[]

from system.mbus import Bus
from system.amqp import AMQPCommTx #@UnresolvedImport

class SensorsHandlerAgent(object):
    
    EXCH="org.sensors"
    
    def __init__(self):
        self.config=None
        self.comm=None
    
    def _hConfig(self, config):
        self.config=config
    
    def _hPoll(self, pc):
        if not self.config:
            Bus.publish(self, "%config-amqp?")
        
        if not self.comm:
            self.comm=AMQPCommTx(self.config, self.EXCH)
            self.comm.connect()
            
        if not self.comm.isOk():
            del self.comm
            self.comm=None

    
    def StateChanged(self, sensor_type, device_id, sensor_name, sensor_state):
        """Generated when a sensor changes state"""
        if self.comm:
            self.comm.publish("state.io.%s" % sensor_type, 
                              {"sensor_type": sensor_type,
                               "device_id": device_id, 
                                "sensor_name": sensor_name, 
                                "sensor_state": sensor_state})

    def ConfigSensors(self, config):
        """Generated when sensor configuration changess and
            also periodically
        """
        if self.comm:
            self.comm.publish("config", config)
    

_shandler=SensorsHandlerAgent()
Bus.subscribe("%config-amqp",    _shandler._hConfig)
Bus.subscribe("%state-changed",  _shandler.StateChanged)
Bus.subscribe("%config-sensors", _shandler.ConfigSensors)
Bus.subscribe("%poll",           _shandler._hPoll)

