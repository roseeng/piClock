#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import pygame
import time
import random
import math
from trelloCalThreaded import TrelloCalThread
from gpioThread import GpioThread
from tempThreaded import TempThread
from piClock import piClock

import pprint
pp = pprint.PrettyPrinter(indent=4)

#
# Main program starts here
#

# Start the power manager thread
gpio = GpioThread()
gpio.daemon = True
gpio.start()

# Start the trello thread
trello = TrelloCalThread()
trello.daemon = True
trello.start()

# Start the thermometer thread
termo = TempThread()
termo.daemon = True
termo.start()

success1 = True
success2 = True
events = []
temp_text = ' '
text_ix = 0 
last_t = 0 # Used to do stuff only once

scope = piClock()
while 1:
    tm = time.localtime()
    t = tm.tm_sec
#    print t
    scope.clear_dial()

    # Once a minute, look for events:
    if t == 0 and t != last_t:
	print "Get Trello"
        success1, events = trello.getEvents()

    # Every 10s, get the temperature:
    if t % 10 == 0 and t != last_t:
        success2, temp = termo.getTemp()
        if success2:
            temp_text = 'Temp: ' + str(temp) + ' C'
        else:
            temp_text = 'Temp: ' + str(temp) 

    # Every 10s, update the texts
    if t % 10 == 0 and t != last_t:
        scope.clear()
        scope.draw_timenum()
        time_text = scope.get_timetext()

        if success1 and success2:
            texts = [ time_text ] + [ temp_text ] + events
        elif not success1:
            texts = events # Only an error text
        elif not success2:
            texts = [ temp_text ] # Only an error text

        if text_ix >= len(texts):
            text_ix = 0
        print "text_ix is: {0}, len is {1}".format(text_ix, len(texts)) 
	pp.pprint(texts)
        text = texts[text_ix]
        scope.draw_timetext(text)
        text_ix = text_ix+1

    scope.draw_dial()
    scope.draw_hands(tm)
    scope.draw_zone2(tm)
    pygame.display.update()
    time.sleep(0.1)
    last_t = t

# end main loop



