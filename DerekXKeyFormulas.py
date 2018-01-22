'''''''''''''''''''''''''''''''''''''''''''''
Derek Xu
ICS3U1 Summative File
Class containing functions for key calculations
Python version 3.6.1
'''''''''''''''''''''''''''''''''''''''''''''

from math import *

def dist(refX,refY,targX,targY):       #Function for finding the distance between
    dX = targX-refX                         #two points. Order is arbitrary
    dY = targY-refY
    distance = sqrt(dX**2+dY**2)
    return distance

def polarAngle(refX,refY,targX,targY):     #Function for finding the polar angle
    dX = targX-refX                             #of a point relative to another
    dY = targY-refY
    angle = atan2(dY,dX)
    return angle                 #**angle in radians**

def xLocation(angle,screenwidth):           #Returns a the horizontal location for a pseudo-3d object
    angle %= (2*pi)
    screenLocation = round((angle - pi)/pi*2*screenwidth)
    return screenLocation

def collide(x1,y1,x2,y2,r):
    if dist(x1,y1,x2,y2) <= r:
        return True
    else:
        return False