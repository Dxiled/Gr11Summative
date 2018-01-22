'''''''''''''''''''''''''''''''''''''''''''''
Derek Xu
ICS3U1 Summative File
Class containing functions for random map generation
Python version 3.6.1
'''''''''''''''''''''''''''''''''''''''''''''

from random import *
from DerekXKeyFormulas import *

class gameMap(object):
    def __init__(self):
        self.wallList = []      #Walls in the form (x,y,horizontalBoolean)
    
    def wallGen(self,player,amount,maxDist):
        for count in range(amount):
            playerDist = randint(50,700)
            angle = randint(0,63)*pi/64
            x = player.X + round(playerDist*cos(angle))
            y = player.Y + round(playerDist*sin(angle))
            self.wallList.append([x,y])
    
    def wallSort(self,player):
        for wall in self.wallList:
            wall = [dist(player.X,player.Y,wall[0],wall[1])] + wall
        self.wallList.sort(reverse=True)
        for wall in self.wallList:
            del wall[0]
    
    def wallWrap(self,player):
        for wall in self.wallList:
            if dist(wall[0],wall[1],player.X,player.Y):
                playerDist = randint(50,700)
                angle = randint(0,63)*pi/64
                x = player.X + round(playerDist*cos(angle))
                y = player.Y + round(playerDist*sin(angle))
                wall = [x,y]
    
    def killMap(self):
        self.wallList = []