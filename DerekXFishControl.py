'''''''''''''''''''''''''''''''''''''''''''''
Derek Xu
ICS3U1 Summative File
Class containing all functions for fish control
Python version 3.6.1
'''''''''''''''''''''''''''''''''''''''''''''

from math import *          #Imports the stuff
from random import *
from DerekXKeyFormulas import *

class fish(object):         #Defines fish class
    def __init__(self):     #Initializes attributes for the fish
        self.X = 0
        self.Y = 0
        self.alive = False
        self.contaminated = False
        self.countDown = randint(0,210)
        self.angle = 0
        self.distance = 0
        self.xLocation = 0
    
    def spawn(self,player):     #Spawns the fish based on the player's location
        self.distance = randint(300,500)    #At a random distance and angle
        angle = randint(0,63)*pi/64
        self.angle = pi + angle             #Faces the fish in the player's general direction
        self.X = player.X + round(self.distance*cos(angle))
        self.Y = player.Y + round(self.distance*sin(angle))
        self.alive = True
        clean = randint(0,5)    #Generates contamination randomly
        if clean:
            self.contaminated = False
        else:
            self.contaminated = True
    
    def kill(self):         #Kills the fish, sets a countdown for its respawn
        self.alive = False
        self.X = 0
        self.Y = 0
        self.countDown = randint(100,300)
    
    def autoMove(self,player,wallList):     #Moves the fish, returns the distance
        if self.alive:
            self.X += round(.7*cos(self.angle))
            self.Y += round(.7*sin(self.angle))
            self.distance = dist(self.X,self.Y,player.X,player.Y)
            if self.distance > 700:             #If the fish gets too far, kills the fish
                self.kill()
        else:
            self.countDown -= 1