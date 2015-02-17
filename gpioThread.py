import hdmiPower
from threading import Thread
import time

class GpioThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.prevHour = -1
        self.hdmi = hdmiPower.hdmiPower()

    def run(self):
        while True:
            tm = time.localtime()
            if self.prevHour != tm.tm_min:
                print "Ny timme"
                if self.inZone(tm):
                    print "Power on"
                    self.hdmi.powerOn()
                else:
                    print "Power off"
                    self.hdmi.powerOff()            
                self.prevHour = tm.tm_min

            time.sleep(4)

    def inZone(self, tm):
        return tm.tm_min % 2 == 1
        
    def cleanup(self):
        print "Resetting hdmi status"
        self.hdmi.powerOn()
