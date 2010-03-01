"""
    LogLimiter module
    
    Limits the rate of logging of events
    
    @author: jldupont

    Created on 2010-02-26
"""
__all__=[]

from system.mbus import Bus


class LogLimiter(object):
    """
    Defaults to no limit when
    no configuration is available for
    a particular `ltype`
    
    Eg. For `ltype X` , msg rate is 1 every Y polls max
    """
    DEFAULT_CDELTA = 0
    
    def __init__(self):
        ## dict of {ltype -> rate}
        self.map={}
        
        ## dict of {ltype -> poll_count_last_logged}
        self.st={}
        
        ## count per type
        self.lc={}
        
        ## current poll count
        self.cpoll=0
    
    def _hllconfig(self, *p):
        """ Log Limiter Configuration
        
            Either: 
            @param key:   key
            @param value: value
            or:
            @param dic: dictionary  
        """
        dic={}
        try:     dic[p[0]]=p[1]
        except:  dic=p[0]
        self.map.update(dic)
    
    def _hpoll(self, pc):
        self.cpoll=pc
    
    def _hllog(self, ltype, *p):
        
        c=self.lc.get(ltype, 0)+1
        self.lc[ltype]=c
        
        try: level, msg = p 
        except:
            level="info"
            try:    msg = p[0]
            except: raise RuntimeError("LogLimiter: invalid usage")
            
        cdelta=self.map.get(ltype, self.DEFAULT_CDELTA)
        lpoll=self.st.get(ltype, 0)
        delta=self.cpoll - lpoll

        #print "cpoll(%s) ltype(%s) delta(%s) cdelta(%s) msg(%s)" % (self.cpoll, ltype, delta, cdelta, msg)
        if delta >= cdelta or lpoll==0:
            self.st[ltype] = self.cpoll
            Bus.publish(self, "%log", level, "(%s:%s) %s" % (ltype, c, msg))
            
    
    
_ll=LogLimiter()
Bus.subscribe("%llog",     _ll._hllog)
Bus.subscribe("%llconfig", _ll._hllconfig)
Bus.subscribe("%poll",     _ll._hpoll)


## ======================================================================
## ======================================================================

if __name__=="__main__":
    
    Bus.debug=True
    
    Bus.publish(None, "%llog", "l1", "info",    "msg1")
    Bus.publish(None, "%llog", "l2", "warning", "msg2")
    Bus.publish(None, "%llog", "l3", "msg3")
    