#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import pygame
import time
import random
import math
import urllib2
from icalendar import Calendar, Event
from threading import Thread
import threading
#import time

class TrelloCalThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.success = False
        self.events = []
        self.dlock = threading.Lock()

    def run(self):
        while True:
            self.fetchEvents()
            time.sleep(10*30)

    def getEvents(self):
        if (self.dlock.acquire(False)):  
            success = self.success
            events = self.events
            self.dlock.release()
        return success, events

    def fetchEvents(self):
        success = False
        events = []

        print "fetching..."
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

#                diff = date - tm
#                if diff.days != 0:
#                    continue
                if date.dt.year != tm.tm_year or date.dt.month != tm.tm_mon or date.dt.day != tm.tm_mday:
                    continue

                events.append(summary)
            success = True

        print "fetch done."
        if (self.dlock.acquire()):  
            self.success = success
            self.events = events
            self.dlock.release()
        print "data saved."




