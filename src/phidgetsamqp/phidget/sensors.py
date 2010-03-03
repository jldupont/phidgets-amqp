"""
    Sensors

    - Publishes configuration data on DBus
    - Intercept "Din", "Dout", "Ain" DBus signals,
        perform a look-up in the configuration data,
        map the result to "/Sensors/State/Changed"
    
    @author: jldupont

    Created on 2010-02-24
"""
__all__=[]

from system.mbus import Bus


class SensorsAgent(object):
    def __init__(self):
        self.map={}
        self.config={}
        self.states={}
    
    ## ==================================================
    
    
    def hConfig(self, config):
        self.config=config
        self.states=config.get("states", None) or config.get("States", None)
    
    def hPinMap(self, map):
        self.map=map
    
    ## ==================================================
    
    def _hDin(self, dic):
        self.processChange("din", dic)
    
    def _hDout(self, dic):
        self.processChange("dout", dic)        

    def _hAin(self, dic):
        self.processChange("ain", dic)

    ## ==================================================
    
    def processChange(self, iotype, dic):
        serial=dic["serial"]
        pin=dic["pin"]
        value=dic["value"]
        pname, mval=self.domap(serial, iotype, pin, value)
        dic.update({"sensor_name": pname, "sensor_state": mval})
        if mval is not None:
            Bus.publish(self, "%state-changed", iotype, dic)
    
    def domap(self, serial, ptype, pin, value):
        pn=self.pmap(serial, ptype, pin)
        pstates=self.states.get(pn, {})
        mvalue=pstates.get(value, None)
        return (pn, mvalue)
        

    def pmap(self, serial, ptype, pin):
        key="%s.%s.%s" % (serial, ptype, pin)
        return self.map.get(key, None)
    

    
_sa=SensorsAgent()
Bus.subscribe("%config-sensors", _sa.hConfig)
Bus.subscribe("%pin-map",        _sa.hPinMap)
Bus.subscribe("%din",  _sa._hDin)
Bus.subscribe("%dout", _sa._hDout)
Bus.subscribe("%ain",  _sa._hAin)
