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
        self.success = True
        self.events = []
	self.errors = 0
        self.dlock = threading.Lock()

    def run(self):
        while True:
            self.fetchEvents()
            time.sleep(5*60)

    def getEvents(self):
        if (self.dlock.acquire(False)):  
            success = self.success
            events = self.events
            self.dlock.release()
        return success, events

    def fetchEvents(self):
        success = True
        events = []

        print "fetching Trello..."
        try:
            req = urllib2.Request('https://trello.com/calendar/4f799cb901dd0cdb21208b60/54bbfa544dc869463114231b/caa041a9c31c013c3baa2738f0f3a4aa.ics')
            response = urllib2.urlopen(req, timeout=15)
            data = response.read()
    	except urllib2.URLError as ex:
	    self.errors = self.errors + 1
            print "Vi fick ett URLError: {0} ".format(ex.reason)
	    if self.errors > 15:
		print "Rebooting..."
		restart()
	    elif self.errors > 10:
		print "Error limit reached, next time we reboot"
		events = [ "Prepare for reboot" ] 
            else:
		events = [ "Trello: " + str(ex.reason) ]
	    success = False

    	else:
	    self.errors = 0
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

        if (self.dlock.acquire()):  
            self.success = success
            self.events = events
            self.dlock.release()

        print "Trello fetch done, errors: {0}.".format(self.errors)

# Move this to main when everything works
def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output



