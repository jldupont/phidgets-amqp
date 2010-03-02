""" Config Agent

    Publishes:
    - "%config-sensors" : complete configuration
    - "%pin-map" : dictionary of [device.pin:pin-name]

    @author: jldupont

    Created on 2010-02-24
"""
import os
import yaml #@UnresolvedImport
from system.mbus import Bus

class ConfigAgent(object):
    
    CONFIG_PATH="~/.phidgets-amqp/"
    CONFIG_FILE="sensors.config"
    
    REFRESH_INTERVAL=10
    
    def __init__(self):
        self.count=self.REFRESH_INTERVAL+1 ## force early processing
        self._path=self.CONFIG_PATH+self.CONFIG_FILE
        self.cpath=os.path.expandvars(os.path.expanduser(self._path))
        self.mtime=None
        self.config={}
        
        ## Notification flags
        self.nConfigPath=False
        self.nConfigFile=False

    def log(self, level, msg):
        Bus.publish(self, "%log", level, msg)
        
    def _hpoll(self, *p):
        self.count=self.count+1
        if self.count > self.REFRESH_INTERVAL:
            self.count=0
            self.doRefresh()

    def doRefresh(self):
        try:    statinfo=os.stat(self.cpath)
        except: statinfo=None
            
        ##  st_mode, st_ino, st_dev, st_nlink, st_uid, 
        ##  st_gid, st_size, st_atime, st_mtime, st_ctime
        if not statinfo:
            if not self.nConfigPath:
                self.nConfigPath=True
                self.log("warning", "Configuration file not found(%s)" % self.cpath)
            return
        
        mtime=statinfo.st_mtime
        if self.mtime != mtime:
            self.log("info", "Configuration file changed, mtime(%s)" % mtime)
            self.mtime = mtime
            self.nConfigPath=False
            self._handleChange()
            
    def _handleChange(self):
        """ Configuration file changed - process it
        """
        try:
            file=open(self.cpath, "r")
            contents=file.readlines()
            file.close()
            self.nConfigFile=False
        except Exception,e:
            if not self.nConfigFile:
                self.nConfigFile=True
                self.log("error", "Unable to open & read configuration file(%s) error(%s)" % (self.cpath, e))
            return
        
        self.processConfigFile(contents)
        
    def processConfigFile(self, contents):
        """ Process the contents of the configuration file """
        try:
            config=yaml.load("\n".join(contents))
        except Exception,e:
            self.log("error", "Unable to parse configuration file(%s) error(%s)" % (self.cpath, e))
            return
        
        self.validateConfig(config)       
        
    def validateConfig(self, config):
        """ Validates (as much as possible) the configuration information
            before handing it off
            
            Categories: "States", "Devices"
            Pins: integer
        """
        pinmap={}
        
        try:    devices=config.get("Devices", None) or config["devices"] 
        except:
            self.log("warning", "Configuration file missing 'Devices' section")
            return
        
        try:    states=config.get("States", None) or config["states"] 
        except:
            self.log("warning", "Configuration file missing 'States' section")
            return
            
        pinnames=[]
            
        try:
            for device_name in devices:
                device=devices[device_name]
                
                try: pins = device.get("Pins", None) or device["pins"]
                except:
                    self.log("warning", "Expecting 'pins' entry for Device(%s) in 'Devices' section" % device_name)
                    return
                
                for pin_entry in pins:
                    try:    ptype=pin_entry["type"]
                    except:
                        self.log("warning", "Expecting 'type' field for pin entry, device(%s)" % device)
                        return
                    
                    try:    pindex=pin_entry["pin"]
                    except:
                        self.log("warning", "Expecting 'pin' field for pin entry, device(%s)" % device)
                        return
                    
                    try:    pname=pin_entry["name"]
                    except:
                        self.log("warning", "Expecting 'name' field for pin entry, device(%s)" % device)
                        return

                    try:    _ipin=int(pindex)
                    except:
                        self.log("warning", "Expecting 'integer' value for 'pin' field in pin entry, device(%s)" % device)
                        return

                    pinnames.extend([pname])
                
                    ## stringify for less headache: normalize type
                    m="%s.%s.%s" % (device_name, ptype, pindex)
                    pinmap[m] = pname
        except:
            self.log("warning", "Error whilst validating 'Devices' section of configuration file")
            return
        
        #print "pinnames: ",pinnames
        
        try:
            for pinname in states:
                if not pinname in pinnames:
                    self.log("warning", "Pin name(%s) not found in any 'Device' definition" % pinname)
        except:
            self.log("warning", "Error whilst validating 'States' section of configuration file")
            return
            
        self.config=config
        self.log("info", "Successfully validated configuration file(%s)" % self.cpath)
        Bus.publish(self, "%config-sensors", self.config)
        Bus.publish(self, "%pin-map", pinmap)
    
_ca=ConfigAgent()
Bus.subscribe("%poll", _ca._hpoll)
