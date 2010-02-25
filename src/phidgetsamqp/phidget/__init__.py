"""
    Phidget package
    @author: Jean-Lou Dupont
"""
__all__=["getDeviceDetails"]

def getDeviceDetails(device):
    details={}
    
    ## should at least have serial number
    try:    details["serial"]  = device.getSerialNum()
    except: pass
    
    try:
        details["name"]    = device.getDeviceName()
        details["type"]    = device.getDeviceType()
        details["version"] = device.getDeviceVersion()
        #details["label"]   = device.getDeviceLabel()  # crashes DBus            
    except:
        pass
    
    return details
