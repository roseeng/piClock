#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import pygame
import time
import random
import math
import urllib2
from icalendar import Calendar, Event

def getEvents():

    events = []

    try:
        req = urllib2.Request('http://trello.com/calendar/4f799cb901dd0cdb21208b60/548d8c4cd981b9f590b4547e/90fc54e71d5253fef77d2cbe0eba270e.ics')
        response = urllib2.urlopen(req)
        data = response.read()
    except urllib2.URLError as ex:
        print "URLError: {0} ".format(ex.reason)
    else:
        cal = Calendar.from_ical(data)

        tm = time.localtime()
        for event in cal.walk('vevent'):

            date = event.get('dtstart')
            summary = event.get('summary')

#            diff = date - tm
#            if diff.days != 0:
#                continue
            if date.dt.year != tm.tm_year or date.dt.month != tm.tm_mon or date.dt.day != tm.tm_mday:
                continue

            events.append(summary)
    
    return events



