"""
    api.config
    
    @author: jldupont

    Created on 2010-02-25
"""
import os
import yaml #@UnresolvedImport

from system.mbus import Bus

class ApiConfig(object):
    """ Handles reading & validating
        the configuration file "~/.phidgets-amqp/amqp.config"
    """
    PARAMS=["host", "userid", "password", "virtual_host"]
    
    CONFIG_PATH="~/.phidgets-amqp/"
    CONFIG_FILE="amqp.config"
    
    REFRESH_INTERVAL=10
    
    DEFAULTS = {  "host":         "localhost:5672"
                 ,"userid":       "guest"
                 ,"password":     "guest"
                 ,"virtual_host": "/"
                }
    
    def __init__(self):
        self.count=self.REFRESH_INTERVAL+1 ## force early processing
        self._path=self.CONFIG_PATH+self.CONFIG_FILE
        self.cpath=os.path.expandvars(os.path.expanduser(self._path))
        self.mtime=None
        self.config=self.DEFAULTS
        
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
                self.log("warning", "Configuration file not found(%s) - using defaults" % self.cpath)
                self.useDefaults()
            return
        
        mtime=statinfo.st_mtime
        if self.mtime != mtime:
            self.log("info", "Configuration file changed, mtime(%s)" % mtime)
            self.mtime = mtime
            self.nConfigPath=False
            self._handleChange()
            
        Bus.publish(self, "%config-amqp", self.config)
            
    def useDefaults(self):
        self.config=self.DEFAULTS
        Bus.publish(self, "%config-amqp", self.config)
            
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
                self.log("error", "Unable to open & read configuration file(%s) error(%s) - using defaults" % (self.cpath, e))
                self.useDefaults()
            return
        
        self.processConfigFile(contents)
        
    def processConfigFile(self, contents):
        """ Process the contents of the configuration file """
        try:
            config=yaml.load("\n".join(contents))
        except Exception,e:
            self.log("error", "Unable to parse configuration file(%s) error(%s) - using defaults" % (self.cpath, e))
            self.useDefaults()
            return
        
        self.validateConfig(config)       
        
    def validateConfig(self, config):
        """ Validates (as much as possible) the configuration information
            before handing it off
            
            Categories: "States", "Devices"
            Pins: integer
        """
        for param in self.PARAMS:
            try:    _value=config[param]
            except:
                self.log("warning", "Missing '%s' entry in configuration file(%s)" % (param, self.cpath)) 
                self.usedefaults()
                return
                    
        self.config=config
        self.log("info", "Successfully validated configuration file(%s)" % self.cpath)
        
    
    def _qconfig_amqp(self, *_):
        """ Answers the question `%config-amqp` """
        Bus.publish(self, "%config-amqp", self.config)
        
    
_ac=ApiConfig()
Bus.subscribe("%poll", _ac._hpoll)
Bus.subscribe("%config-amqp?", _ac._qconfig_amqp)
