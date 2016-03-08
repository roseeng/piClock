#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import urllib2
import json
from threading import Thread
import threading
import time

class TempThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.success = False
        self.temp = 0
	self.errors = 0
        self.dlock = threading.Lock()

    def run(self):
        while True:
            self.fetchTemp()
            time.sleep(10*30)

    def getTemp(self):
        if (self.dlock.acquire(False)):  
            success = self.success
            temp = self.temp
            self.dlock.release()
        return success, temp

    def fetchTemp(self):
        success = False
        temp = 0

        print "fetching Temp..."
        try:
            req = urllib2.Request('http://kronos:8081/json.htm?type=devices&rid=23')
            data = json.load( urllib2.urlopen(req))

    	except urllib2.URLError as ex:
	    self.errors = self.errors + 1
	    msg = str(ex.reason)
	    unicode_str = msg.decode("windows-1252")
	    temp = unicode_str.encode("windows-1252")

            print "Vi fick ett URLError: {0} ".format(temp)
    	else:
	    self.errors = 0
            temp = data.get('result')[0].get('Temp')
            success = True
	
        print "Temp fetch done, errors={0}.".format(self.errors)
        if (self.dlock.acquire()):  
            self.success = success
            self.temp = temp
            self.dlock.release()
        print "temp saved."




