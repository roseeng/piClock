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

        print "fetching..."
        try:
            req = urllib2.Request('http://kronos:8080/json.htm?type=devices&rid=23')
            data = json.load( urllib2.urlopen(req))

    	except urllib2.URLError as ex:
            print "Vi fick ett URLError: {0} ".format(ex.reason)
    	else:
            temp = data.get('result')[0].get('Temp')
            success = True
	
        print "fetch done."
        if (self.dlock.acquire()):  
            self.success = success
            self.temp = temp
            self.dlock.release()
        print "temp saved."




