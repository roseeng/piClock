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

    success = False
    events = []

    try:
        req = urllib2.Request('https://trello.com/calendar/4f799cb901dd0cdb21208b60/54bbfa544dc869463114231b/caa041a9c31c013c3baa2738f0f3a4aa.ics')
        response = urllib2.urlopen(req)
        data = response.read()
    except urllib2.URLError as ex:
        print "Vi fick ett URLError: {0} ".format(ex.reason)
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
        success = True

    return success, events



