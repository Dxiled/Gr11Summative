'''''''''''''''''''''''''''''''''''''''''''''
Derek Xu
ICS3U1 Summative File
Class containing all functions for player control
Python version 3.6.1
'''''''''''''''''''''''''''''''''''''''''''''

#Imports necessary modules for player class
from math import *
from pygame import *
from DerekXKeyFormulas import *

init()

class playerControl(object):        #Defines player class
    def __init__(self):                 #Initializes attributes
        self.X = 0
        self.Y = 0
        self.angle = 0
        self.health = 0
        self.decay = 0
        self.alive = False
        self.score = 0
        self.charType = 0
        self.biteTime = 0
    
    def spawn(self,x,y,character):      #Spawns the player in, changing attributes accordingly
        if not self.alive:
            self.alive = True
            self.health = 2000
            self.X = x
            self.Y = y
            self.score = 0
            self.charType = character
            if self.charType == 2:
                self.decay = 3
            elif self.charType == 0:
                self.decay = 2
            else:
                self.decay = 1
    
    def move(self,upkey,leftkey,downkey,rightkey,mouserel):     #Affects the x and y attributes through input
        if self.alive:
            bufferX = self.X
            bufferY = self.Y
            self.angle -= mouserel[0]*pi/2048     
            if self.charType == 0:
                speed = 3
            elif self.charType == 1:
                speed = 2
            else:
                speed = 4
            if upkey:
                for count in range(speed):
                    bufferX += cos(self.angle)
                    bufferY += sin(self.angle)
            if leftkey:
                for count in range(speed):
                    bufferX += cos(self.angle + pi/2)
                    bufferY += sin(self.angle + pi/2)
            if downkey:
                for count in range(speed):
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
    
    def eat(self,target):           #Attempts to eat a fish, showing the bite
        self.biteTime = 1               #Initializes the bite chain reaction
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
    
    def bite(self,window,biteList):         #Shows the biting animation for the appropriate animal
        if self.biteTime in range(1,5):
            self.biteTime += 1      #Uses a variable controlled by the game loop
            window.blit(biteList[self.charType],(0,70*self.biteTime-70))
            window.blit(transform.flip(biteList[self.charType],False,True),(0,700-70*self.biteTime))
        else:
            self.biteTime = 0