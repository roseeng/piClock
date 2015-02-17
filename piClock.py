#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import pygame
import time
import random
import math
import trelloCal
from gpioThread import GpioThread

class piClock :
    screen = None;
    maxx = 0;
    maxy = 0;
    origo = (0, 0);

    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (size[0], size[1])

        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        self.maxx = size[0]
        self.maxy = size[1]
        self.origo = (self.maxx/2, self.maxy/2)

        # Clear the screen to start
        print "Clearing screen..."
        self.clear()   
        # Initialise font support
        print "Init fonts..."
        pygame.font.init()
        # Render the screen
        pygame.display.update()
        print "Init complete."

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def clear(self):
        "Clear screen"
        self.screen.fill((0, 0, 0))        

    def clear_dial(self):
        "Clear the part of the screen with the clock dial"
        radius = min(self.maxx, self.maxy)/2
        dialrect = pygame.Rect(0,0,0,0)
        dialrect.width = 2*radius
        dialrect.height = 2*radius
        dialrect.center = self.origo
        self.screen.fill((0, 0, 0), dialrect)        

    def test(self):
        # Fill the screen with red (255, 0, 0)
        red = (255, 0, 0)
        self.screen.fill(red)
        # Update the display
        pygame.display.update()

    def vect2coord(self, radius, angle):
        # Convert from r,phi to x,y - clockwise 
        x = self.origo[0] + radius*math.sin(math.radians(90-angle))
        y = self.origo[1] + radius*math.cos(math.radians(90-angle))
        return (x, y)

    def draw_dial(self):
        # Draw a clock dial
        radius = min(self.maxx, self.maxy)/2
        color_min = (255, 0, 0)
        color_hour = (0, 0, 255)
        for ang in range(0, 360, 360/60):
            p0 = self.vect2coord(0.9*radius, ang)
            p1 = self.vect2coord(radius, ang)
            pygame.draw.line(self.screen, color_min, p0, p1)
        for ang in range(0, 360, 360/12):
            p0 = self.vect2coord(0.8*radius, ang)
            p1 = self.vect2coord(radius, ang)
            if ang == 0:
                color = color_hour
            else:
                color = color_min
            pygame.draw.line(self.screen, color, p0, p1)
        
    def draw_hands(self, tm):
        # Draw the clock hands
        radius = min(self.maxx, self.maxy)/2
        color_hand = (255, 255, 255)

        hour = tm.tm_hour
        if hour > 12:
            hour = hour -12
        minute = tm.tm_min
        second = tm.tm_sec

        ang = 360 * (hour*60 + minute)/(12*60)
        p = self.vect2coord(0.5*radius, ang)
        pygame.draw.line(self.screen, color_hand, self.origo, p, 5)

        ang = 360 * minute/60
        p = self.vect2coord(0.8*radius, ang)
        pygame.draw.line(self.screen, color_hand, self.origo, p, 3)

        ang = 360 * second/60
        p = self.vect2coord(1.0*radius, ang)
        pygame.draw.line(self.screen, color_hand, self.origo, p, 1)

    zone_start_h = 7
    zone_start_m = 45
    zone_end_h = 8
    zone_end_m = 20

    def draw_zone2(self, tm):
        # Draw a zone (Go to school)
        dminute = tm.tm_hour*60 + tm.tm_min
        zone_start = self.zone_start_h*60 + self.zone_start_m
        zone_end = self.zone_end_h*60 + self.zone_end_m
        if dminute < zone_start or dminute > zone_end:
            return 

        ratio = (dminute-zone_start)*100.0/(zone_end-zone_start)
        if ratio < 30:
            color_zone = (0, 200, 40)
        elif ratio < 70:
            color_zone = (200, 200, 0)
        else:
            color_zone = (200, 0, 0)

#        color_passed_zone = color_zone/1.5

        radius = min(self.maxx, self.maxy)/2
        ang0 = 360 * self.zone_start_m/60
        ang1 = 360 * self.zone_end_m/60
        ang_now = 360 * tm.tm_min/60

        if ang1 < ang0:
            ang0 = ang0-360
        if ang1 < ang_now:
            ang_now = ang_now-360

        for ang in range(ang0, ang1, 5):
            p0 = self.vect2coord(0.5*radius, ang)
            p1 = self.vect2coord(0.7*radius, ang)
 #           if ang < ang_now:
 #               pygame.draw.line(self.screen, color_passed_zone, p0, p1, 5)
 #           else:
            pygame.draw.line(self.screen, color_zone, p0, p1, 5)


    def draw_zone(self, tm):
        # Draw a zone (Go to school)
        dminute = tm.tm_hour*60 + tm.tm_min
        zone_start = self.zone_start_h*60 + self.zone_start_m
        zone_end = self.zone_end_h*60 + self.zone_end_m
        if dminute < zone_start or dminute > zone_end:
            return 

        ratio = (dminute-zone_start)*100.0/(zone_end-zone_start)
        if ratio < 30:
            color_zone = (0, 200, 40)
        elif ratio < 70:
            color_zone = (200, 200, 0)
        else:
            color_zone = (200, 0, 0)

        radius = min(self.maxx, self.maxy)/2
        arcrect = pygame.Rect(0,0,0,0)
        arcrect.width = 2*0.7*radius
        arcrect.height = 2*0.7*radius
        arcrect.center = self.origo
        ang0 = -360 * self.zone_start_m/60
        ang1 = -360 * self.zone_end_m/60
        if ang0 < -360:
            ang0 = ang0+360
        if ang0 < 0:
            ang0 = ang0+360
        if ang1 < -360:
            ang1 = ang1+360
        if ang1 < 0:
            ang1 = ang1+360
        print "Zone from {0} to {1}".format(ang0, ang1)

        if ang1 < ang0:
            ang0 = ang0-360

        pygame.draw.arc(self.screen, color_zone, arcrect, math.radians(ang0), math.radians(ang1), 40)

    def draw_timenum(self):
        # Write time as digits
        radius = min(self.maxx, self.maxy)/2
        font = pygame.font.Font(None, 150)

        timestr = time.strftime("%H:%M")
        surface = font.render(timestr, 1, (0, 0, 255), (0, 0, 0))
        surface = pygame.transform.rotate(surface, -90)
        pos = (1100, 400)
        size = surface.get_height()
        textpos = (pos[0], pos[1]-size/2)
        self.screen.blit(surface, textpos)
 
    def get_timetext(self):
        # Convert time to text
        tm = time.localtime()
        hour = tm.tm_hour
        minute = tm.tm_min
        second = tm.tm_sec

        timestr = u"Klockan är "
        parts = ['', "fem X ", "tio X ", "kvart X ", "tjugo X ", "fem X halv ", "halv "]
        ix = int(round(minute/5.0, 0))
        if ix > 6:
            ixx = 12-ix
        else:
            ixx = ix
        part = parts[ixx]
        if ix < 5 or ix == 7:
            part = part.replace("X", u"över")
        else:
            part = part.replace("X", "i")
        if ix >= 5:
            hour = hour+1

        if hour > 12:
            hour = hour-12

        timestr = timestr + part

        hours = ["tolv", "ett", u"två", "tre", "fyra", "fem", "sex", "sju", u"åtta", "nio", "tio", "elva", "tolv"]
        hourstr = hours[hour]
        timestr = timestr + hourstr
        return timestr

    def draw_timetext(self, str):
        # Write a text
        radius = min(self.maxx, self.maxy)/2
        font = pygame.font.Font(None, 80)

        surface = font.render(str, 1, (0, 0, 255), (0, 0, 0))
        surface = pygame.transform.rotate(surface, -90)
        pos = (100, 400)
        size = surface.get_height()
        textpos = (pos[0], pos[1]-size/2)
        self.screen.blit(surface, textpos)

#
# Main program starts here
#

# Start the power manager thread
th = GpioThread()
th.daemon = True
th.start()

# Get a list of events to show
success, e = trelloCal.getEvents()
if success:
    evs = e
#evs = []
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
        success, e = trelloCal.getEvents()
        if success:
            evs = e



