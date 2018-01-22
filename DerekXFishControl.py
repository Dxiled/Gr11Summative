'''''''''''''''''''''''''''''''''''''''''''''
Derek Xu
ICS3U1 Summative File
Class containing all functions for fish control
Python version 3.6.1
'''''''''''''''''''''''''''''''''''''''''''''

from math import *
from random import *
from DerekXKeyFormulas import *

class fish(object):
    def __init__(self):
        self.X = 0
        self.Y = 0
        self.alive = False
        self.contaminated = False
        self.countDown = randint(0,210)
        self.angle = 0
        self.distance = 0
        self.xLocation = 0
    
    def spawn(self,player):
        self.distance = 300
        angle = randint(0,63)*pi/64
        self.angle = pi + angle
        self.X = player.X + round(self.distance*cos(angle))
        self.Y = player.Y + round(self.distance*sin(angle))
        self.alive = True
        clean = randint(0,5)
        if clean:
            self.contaminated = False
        else:
            self.contaminated = True
    
    def kill(self):
        self.alive = False
        self.X = 0
        self.Y = 0
        self.countDown = randint(300,600)
    
    def autoMove(self,player,wallList):
        if self.alive:
            self.X += round(.7*cos(self.angle))
            self.Y += round(.7*sin(self.angle))
            self.distance = dist(self.X,self.Y,player.X,player.Y)
            if self.distance > 700:
                self.kill()
        else:
            self.countDown -= 1