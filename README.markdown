This project consists of an AMQP API to [Phidgets](http://www.phidgets.com/) devices. 

Applications
------------

- "phidgets-amqp-manager" : publishes the messages "Attached", "Detached", "Error" and "Devices" 

- "phidgets-amqp-ifk" : publishes the messages "Din", "Dout", "Ain" and "Error" 

- "phidgets-amqp-sensors" : publishes the message "State" which reflects the current state of an input. 
  This application must be configured through "sensors.config" file located in "~/.phidgets-amqp" directory.

The latter ("phidgets-amqp-ifk") requires "phidgets-amqp-manager" to be running: it subscribes to the "Devices"
signal in order to be notified of new "InterfaceKit" devices to service.

AMQP Exchanges
--------------

The applications use the following exchanges:

- "com.phidgets"
- "org.sensors"

Messages Types
--------------

On the "com.phidgets" exchange, there are the following message keys:

- "device.state.attached"
- "device.state.detached"
- "device.state.error"
- "device.io.din"
- "device.io.dout"
- "device.io.ain"

On the "org.sensors" exchange, there are the following message keys:

- "state.io"

Message Format
--------------



AMQP Configuration
==================

If the defaults aren't satisfactory, the file "~/.phidgets-amqp/amqp.config" (YAML format)
can be customized. It is checked for modification(s) at regular interval and reloaded if need be.

The following parameters are supported:
* host
* userid
* password
* virtual_host

Example:

## Using YAML "maps"
host:          "localhost:5672"
userid:       "joe"
password:     "blo"
virtual_host: "\"

Sensors configuration
=====================

Example "sensors.config" file (YAML syntax):

Devices:

 ## Device unique id i.e. serial
 80860:
  pins:
   3: porte_fournaise
   4: porte_escalier
   0: porte_garage_1
   1: porte_garage_2

States:
 porte_escalier:
  0: Open
  1: Closed
 porte_garage_1:
  0: Open
  1: Closed
 porte_garage_2:
  0: Open
  1: Closed
 porte_fournaise:
  0: Open
  1: Closed


Installation
============
There are 2 methods:

1. Use the Ubuntu Debian repository [jldupont](https://launchpad.net/~jldupont/+archive/phidgets)  with the package "rbsynclastfm"

2. Use the "Download Source" function of this git repo and use "sudo make install"

Dependencies
============

* python-amqplib
* Phidgets Library (available in the PPA)
* Python Phidgets Library (available in the PPA)
