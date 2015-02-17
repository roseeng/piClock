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

flagFile = "/run/shm/hdmi_power_off"
hdmiOn = True
if os.path.exists(flagFile):
    hdmiOn = False
    print "OS indicates HDMI was off"

def powerOn():
    if hdmiOn:
        print "HDMI already on"
    else:
        toggle()
        os.remove(flagFile)

def powerOff():
    if hdmiOn:
        toggle()
        open(flagFile, 'a').close()
    else:
        print "HDMI already off"

def toggle():
    GPIO.setup(25, GPIO.OUT, initial=1)
    GPIO.output(25, 0)         # this is our simulated button press
    sleep(0.2)                 # hold button for 0.2 seconds
    GPIO.output(25, 1)         # release button
    GPIO.setup(25, GPIO.IN)    # set port back to input (re-enables buttons)
 
if __name__ == "__main__":
    import sys
    if sys.argv[1] == "on":
        powerOn()
    if sys.argv[1] == "off":
        powerOff()
    GPIO.cleanup()

