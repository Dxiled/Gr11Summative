'''''''''''''''''''''''''''''''''''''''''''''
Derek Xu
ICS3U1 Summative File
Class containing all functions for background items
Python version 3.6.1
'''''''''''''''''''''''''''''''''''''''''''''

from random import *        #Imports the stuff I need
from pygame import *

class bgObject(object):     #Defines background class
    
    def __init__(self):             #Initializes background object
        self.X = randint(0,700)
        self.Y = randint(575,800)
        self.item = randint(0,3)
        self.imageList = [image.load('DerekXShell.png'),image.load('DerekXKelp.png'),image.load('DerekXClam.png'),image.load('DerekXRock.png')]
        self.size = self.Y - 540
    
    def move(self,forward,left,backward,right,mouse):      #Moves objects based on movement of the player
        if forward:            #Up and down the screen if moving forward or backward
            self.Y += 2
            if self.Y > 800:
                self.X = randint(0,700)
                self.Y = 575
                self.item = randint(0,3)
        elif backward:
            self.Y -= 2
            if self.Y < 575:
                self.X = randint(0,700)
                self.Y = 800 
                self.item = randint(0,3)
        self.X -= mouse     #Moves the stuff when the player turns
        if left:            #Moves the stuff as the player strafes
            self.X += 2
        if right:
            self.X -= 2
        if self.X < -100:   #Wraps the item around horizontally
            self.X = 700
            self.Y = randint(575,800)
            self.item = randint(0,3)
        elif self.X > 700:
            self.X = -100
            self.Y = randint(575,800)
            self.item = randint(0,3)
        self.size = self.Y - 540
    
    def draw(self,screen):      #Draws the thing based on a generated type
        displayItem = transform.scale(self.imageList[self.item],(self.size,self.size))
        if self.Y < 600:
            displayItem = displayItem.convert()
            displayItem.set_alpha(((self.Y-575)*.63)**2)
            displayItem.set_colorkey((255,255,255))
        screen.blit(displayItem,(self.X,self.Y))