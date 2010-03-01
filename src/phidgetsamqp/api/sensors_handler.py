"""
    Sensors - AMQP interface
    
    @author: jldupont

    Created on 2010-02-24
"""
__all__=[]

from system.mbus import Bus


class SensorsState(object):
    """
    DBus signals handler
    """
    PATH    = "/State"
    BUS_NAME= "org.sensors"
    INTERF  = "org.sensors"
    
    def __init__(self):
        pass
    
    def State(self, device_id, sensor_name, sensor_state):
        """Generated when a sensor changes state"""
    

_shandler=SensorsState()
Bus.subscribe("%state-changed", _shandler.State)


class SensorsConfig(object):
    """
    DBus signals handler
    """
    PATH    = "/Config"
    BUS_NAME= "org.sensors"
    INTERF  = "org.sensors"
    
    def __init__(self):
        pass
        
    def Sensors(self, config):
        """Generated when sensor configuration changess and
            also periodically
        """
    

_chandler=SensorsConfig()
Bus.subscribe("%config-sensors", _chandler.Sensors)

