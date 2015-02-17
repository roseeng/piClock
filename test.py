from gpioThread import GpioThread
from time import sleep

print "Start!"

th = GpioThread()
th.daemon = True
th.start()

print "Starting main loop"
for i in range(18):
    print "One step in the main loop"
    sleep(8)

print "Done."


