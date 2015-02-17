#!/usr/bin/env python2.7  
# HDMIPi_toggle.py by Alex Eames http://raspi.tv/?p=7540 
import RPi.GPIO as GPIO
from time import sleep
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN)
 
# If 25 is set as an input, the hardware pullup on the HDMIPi board 
# keeps value at HIGH. We only change the port to an output when we 
# want to toggle the button. 
# This is because, when set as an output, the HDMIPi buttons are disabled.
# So each time we toggle the HDMIPi on or off, we set port back to input

class hdmiPower():

    def __init__(self):
        self.flagFile = "/run/shm/hdmi_power_off"
        self.hdmiOn = True
        if os.path.exists(self.flagFile):
            self.hdmiOn = False
            print "OS indicates HDMI was off"
        else:
            print "OS indicates HDMI was on"

    def powerOn(self):
        if self.hdmiOn:
            print "HDMI already on"
        else:
            self.hdmiOn = True
            self.toggle()
            os.remove(self.flagFile)

    def powerOff(self):
        if self.hdmiOn:
            self.hdmiOn = False
            self.toggle()
            open(self.flagFile, 'a').close()
        else:
            print "HDMI already off"

    def toggle(self):
        GPIO.setup(25, GPIO.OUT, initial=1)
        GPIO.output(25, 0)         # this is our simulated button press
        sleep(0.2)                 # hold button for 0.2 seconds
        GPIO.output(25, 1)         # release button
        GPIO.setup(25, GPIO.IN)    # set port back to input (re-enables buttons)
 
if __name__ == "__main__":
    import sys

    hdmi = hdmiPower()
    if sys.argv[1] == "on":
        hdmi.powerOn()
    if sys.argv[1] == "off":
        hdmi.powerOff()

    GPIO.cleanup()

