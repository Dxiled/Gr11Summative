'''''''''''''''''''''''''''''''''''''''''''''
Derek Xu
ICS3U1 Summative File
Class containing all functions for player control
Python version 3.6.1
'''''''''''''''''''''''''''''''''''''''''''''

from math import *
from DerekXKeyFormulas import *

class playerControl(object):
    def __init__(self):
        self.X = 0
        self.Y = 0
        self.angle = 0
        self.health = 0
        self.decay = 0
        self.alive = False
        self.score = 0
    
    def spawn(self,x,y):
        if not self.alive:
            self.alive = True
            self.health = 2000
            self.decay = 1
            self.X = x
            self.Y = y
            self.score = 0
    
    def move(self,upkey,leftkey,downkey,rightkey,mouserel,wallList):
        if self.alive:
            bufferX = self.X
            bufferY = self.Y
            self.angle -= mouserel[0]*pi/2048           
            if upkey:
                for count in range(2):
                    bufferX += cos(self.angle)
                    bufferY += sin(self.angle)
            if leftkey:
                for count in range(2):
                    bufferX += cos(self.angle + pi/2)
                    bufferY += sin(self.angle + pi/2)
            if downkey:
                for count in range(2):
                    bufferX += cos(self.angle - pi)
                    bufferY += sin(self.angle - pi)
            if rightkey:
                for count in range(2):
                    bufferX += cos(self.angle - pi/2)
                    bufferY += sin(self.angle - pi/2)
            self.X = round(bufferX)
            self.Y = round(bufferY)
            self.angle %= 2*pi
    
    def get_health(self):
        if self.alive:
            self.health -= self.decay
            if self.health <= 0:
                self.X = 0
                self.Y = 0
                self.alive = False
    
    def eat(self,target):
        if dist(self.X,self.Y,target.X,target.Y) < 25:
            angle = (polarAngle(self.X,self.Y,target.X,target.Y) - self.angle)%(2*pi)
            if angle < pi/4 or angle > 1.75*pi:
                target.kill()
                self.score += 1
                if self.health <= 1800:
                    self.health += 200
                else:
                    self.health = 2000
                if target.contaminated:
                    self.decay += 1