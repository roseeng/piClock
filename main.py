#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import pygame
import time
import random
import math
from trelloCalThreaded import TrelloCalThread
from gpioThread import GpioThread
from piClock import piClock

#
# Main program starts here
#

evs = []

# Start the power manager thread
gpio = GpioThread()
gpio.daemon = True
gpio.start()

# Start the trello thread
trello = TrelloCalThread()
trello.daemon = True
trello.start()

# Get a list of events to show
success, e = trello.getEvents()
if success:
    evs = e

print evs
evix = 0 
disp = 1

scope = piClock()
while 1:
    tm = time.localtime()
    t = tm.tm_sec
#    print t
    scope.clear_dial()
    if t % 10 == 0:
        if disp:
            scope.clear()
            scope.draw_timenum()
            t_text = scope.get_timetext()
            texts = [ t_text ] + evs
            text = texts[evix]
            print text
            scope.draw_timetext(text)
            evix = evix+1
            if evix >= len(texts):
                evix = 0
            disp = 0
    else:
        disp = 1

    scope.draw_dial()
    scope.draw_hands(tm)
    scope.draw_zone2(tm)
    pygame.display.update()
    time.sleep(0.1)
    if t == 0:
        success, e = trello.getEvents()
        if success:
            evs = e



