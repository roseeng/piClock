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
            if self.prevHour != tm.tm_hour:
                print "Ny timme"
                if self.inZone(tm):
                    print "Power on"
                    self.hdmi.powerOn()
                else:
                    print "Power off"
                    self.hdmi.powerOff()            
                self.prevHour = tm.tm_hour

            time.sleep(4)

    def inZone(self, tm):
        hour = tm.tm_hour
        return (hour >= 6 and hour < 10) or (hour >= 14 and hour < 22)
        
    def cleanup(self):
        print "Resetting hdmi status"
        self.hdmi.powerOn()
