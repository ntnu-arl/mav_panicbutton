# USB Panic Button interface code
# Copyright 2010 Ken Shirriff
# http://arcfn.com
#
""" PanicButton - interface to USB Panic Button

This code requires PyUSB.
"""

import usb.core

class PanicButton:
  def __init__(self):
    # Device is: ID 1130:0202 Tenx Technology, Inc. 
    self.dev = usb.core.find(idVendor=0x1130, idProduct=0x0202)
    if not self.dev:
      raise ValueError("Panic Button not found")
    
    try:
      self.dev.detach_kernel_driver(0) # Get rid of hidraw
    except Exception, e:
      pass # already unregistered
    
    c = 1
    for config in self.dev:
       print 'config', c
       print 'Interfaces', config.bNumInterfaces
       for i in range(config.bNumInterfaces):
         if self.dev.is_kernel_driver_active(i):
            self.dev.detach_kernel_driver(i)
         print i
       c+=1
    self.dev.set_configuration()

  def read(self):
    """ Read the USB port.
    Return 1 if pressed and released, 0 otherwise.
    """
    #Magic numbers are from http://search.cpan.org/~bkendi/Device-USB-PanicButton-0.04/lib/Device/USB/PanicButton.pm
    return self.dev.ctrl_transfer(bmRequestType=0xA1, bRequest=1, wValue=0x300, data_or_wLength=8, timeout=500)[0]
    
if __name__ == "__main__":
  import time
  button = PanicButton()
  while 1:
    if button.read():
      print "Pressed"
    time.sleep(.5)
