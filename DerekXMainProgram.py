'''''''''''''''''''''''''''''''''''''''''''''
Derek Xu
ICS3U1 Summative File
Main Program
Python version 3.6.1
'''''''''''''''''''''''''''''''''''''''''''''

from math import *
from random import *
from pygame import *
import os 
#Every module beyond here is of my own creation
from DerekXPlayerControl import *
from DerekXFishControl import *
from DerekXKeyFormulas import *
from DerekXGameMap import *
from DerekXBackgroundObjects import *

init()

os.environ['SDL_VIDEO_CENTERED'] = '1'

def drawBackground(window,player,image,stuff,up,left,down,right,sides,screenwidth):
    backgroundX = xLocation(player.angle,100*ceil(screenwidth/100))
    backgroundX %= 100
    for x in range(-100,100*ceil(screenwidth/100),100):
        screen.blit(image,(x+backgroundX,0))
    for thing in stuff:
        thing.move(up,left,down,right,sides)
    stuff.sort(key=lambda thing:thing.Y)
    for thing in stuff:
        thing.draw(window)

def drawHealth(window,health):
    draw.rect(window,(255,0,0),(50,50,400,50))
    draw.rect(window,(0,255,0),(50,50,health//5,50))

def drawScore(window,score):
    scoreString = "Score: " + str(score)
    scoreRender = scoreFont.render(scoreString,False,(0,100,0))
    screen.blit(scoreRender,(650-scoreRender.get_width(),60))

def drawHighscore(window):
    docR = open("DerekXHighscore.dat",'r')
    highscore = docR.readline()
    docR.close()
    highscoreRender = scoreFont.render("Highscore: " + highscore,False,(0,0,0))
    screen.blit(highscoreRender,(350 - highscoreRender.get_width()//2,200))

screen = display.set_mode((700,700))
clock = time.Clock()
secondTick = 0

player = playerControl()

fishList = []

for count in range(10):
    buffer = fish()
    fishList.append(buffer)

running = True
w = False
a = False
s = False
d = False
clicking = False

background = image.load("DerekXBackground.png")
title = image.load("DerekXTitle.png")
healthyFish = [image.load("DerekXFish1Back.png"),image.load("DerekXFish1BackLeft.png"),image.load("DerekXFish1Left.png"),image.load("DerekXFish1FrontLeft.png"),image.load("DerekXFish1Front.png"),image.load("DerekXFish1FrontRight.png"),image.load("DerekXFish1Right.png"),image.load("DerekXFish1BackRight.png")]
unhealthyFish = [image.load("DerekXFish2Back.png"),image.load("DerekXFish2BackLeft.png"),image.load("DerekXFish2Left.png"),image.load("DerekXFish2FrontLeft.png"),image.load("DerekXFish2Front.png"),image.load("DerekXFish2FrontRight.png"),image.load("DerekXFish2Right.png"),image.load("DerekXFish2BackRight.png")]
instructions = [image.load("DerekXInstructions1.png"),image.load("DerekXInstructions2.png"),image.load("DerekXInstructions3.png")]

backgroundObjects = []
for count in range(10):
    buffer = bgObject()
    backgroundObjects.append(buffer)

menuButton1 = Rect(200,300,300,50)
menuButton2 = Rect(200,400,300,50)
menuButton3 = Rect(200,500,300,50)
backButton = Rect(50,600,100,50)
nextButton = Rect(550,600,100,50)

menuFont = font.SysFont("ocraii",40)
scoreFont = font.SysFont("ocraii",30)

playText = menuFont.render("Play",False,(0,0,100))
instructionText = menuFont.render("How to Play",False,(0,0,100))
quitText = menuFont.render("Quit",False,(100,0,0))
resumeText = menuFont.render("Resume",False,(0,0,100))
mainMenuText = menuFont.render("Main Menu",False,(100,0,0))
nextText = menuFont.render("Next",False,(0,0,0))
backText = menuFont.render("Back",False,(0,0,0))

playWidth = playText.get_width()
instructionWidth = instructionText.get_width()
quitWidth = quitText.get_width()
resumeWidth = resumeText.get_width()
mainMenuWidth = mainMenuText.get_width()
nextWidth = nextText.get_width()
backWidth = backText.get_width()

instructionState = 0

MENU = 0
GAME = 1
PAUSE = 2
INSTRUCTION = 3

mode = MENU

while running:
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False
        if evnt.type == KEYDOWN:
            if evnt.key == K_w:
                w = True
            if evnt.key == K_a:
                a = True
            if evnt.key == K_s:
                s = True
            if evnt.key == K_d:
                d = True
            if evnt.key == K_ESCAPE:
                if mode == GAME:
                    mode = PAUSE
        if evnt.type == KEYUP:
            if evnt.key == K_w:
                w = False
            if evnt.key == K_a:
                a = False
            if evnt.key == K_s:
                s = False
            if evnt.key == K_d:
                d = False
        if evnt.type == MOUSEBUTTONDOWN:
            if evnt.button == 1:
                clicking = True
    
    if mode == MENU:
        mouse.set_visible(True)
        for x in range(0,601,100):
            screen.blit(background,(x,0))
        screen.blit(title,(205,75))
        draw.rect(screen,(0,0,200),menuButton1)
        draw.rect(screen,(0,0,200),menuButton2)
        draw.rect(screen,(200,0,0),menuButton3)
        mousePos = mouse.get_pos()
        if menuButton1.collidepoint(mousePos):
            draw.rect(screen,(0,0,255),menuButton1)
            if clicking:
                mode = GAME
                for fish in fishList:
                    fish.kill()
                    fish.countDown -= 300
                    player.alive = False
                    player.spawn(350,350)
        elif menuButton2.collidepoint(mousePos):
            draw.rect(screen,(0,0,255),menuButton2)
            if clicking:
                mode = INSTRUCTION
        elif menuButton3.collidepoint(mousePos):
            draw.rect(screen,(255,0,0),menuButton3)
            if clicking:
                running = False
        drawHighscore(screen)
        screen.blit(playText,(350-playWidth//2,305))
        screen.blit(instructionText,(350-instructionWidth//2,405))
        screen.blit(quitText,(350-quitWidth//2,505))
    
    elif mode == GAME:
        mouse.set_visible(False)
        for fish in fishList:
            if not fish.alive:
                if fish.countDown == 0:
                    fish.spawn(player)
            
            fish.autoMove(player,[])
            fish.xLocation = xLocation(pi - polarAngle(player.X,player.Y,fish.X,fish.Y) + player.angle,700) + 350
    
        
        if clicking:
            for fish in fishList:
                player.eat(fish)
        
        mouseMovement = (mouse.get_pos()[0] - 350,mouse.get_pos()[1] - 350)
        mouse.set_pos([350,350])
        
        player.move(w,a,s,d,mouseMovement,[])
        player.get_health()
        if not player.alive:
            mode = MENU
            docR = open("DerekXHighscore.dat",'r')
            highscore = int(docR.readline())
            docR.close()
            print(highscore,'/',player.score)
            if player.score > highscore:
                docW = open("DerekXHighscore.dat",'w')
                docW.write(str(player.score))
                docW.close()
        
        secondTick += 1
        secondTick %= 60
        
        drawBackground(screen,player,background,backgroundObjects,w,a,s,d,mouseMovement[0],700)
        
        drawHealth(screen,player.health)
        drawScore(screen,player.score)
        
        fishList.sort(key=lambda fish:fish.distance,reverse=True)
        for fish in fishList:
            if fish.alive:
                angle = ((fish.angle)%(2*pi) - (player.angle)%(2*pi))%(2*pi)
                if fish.contaminated:
                    if angle <= pi/8 or angle >= 1.875*pi:
                        fishRender = unhealthyFish[0].convert()
                    elif angle <= .375*pi:
                        fishRender = unhealthyFish[1].convert()
                    elif angle <= .625*pi:
                        fishRender = unhealthyFish[2].convert()
                    elif angle <= .875*pi:
                        fishRender = unhealthyFish[3].convert()
                    elif angle <= 1.125*pi:
                        fishRender = unhealthyFish[4].convert()
                    elif angle <= 1.375*pi:
                        fishRender = unhealthyFish[5].convert()
                    elif angle <= 1.625*pi:
                        fishRender = unhealthyFish[6].convert()
                    else:
                        fishRender = unhealthyFish[7].convert()
                else:
                    if angle <= pi/8 or angle >= 1.875*pi:
                        fishRender = healthyFish[0].convert()
                    elif angle <= .375*pi:
                        fishRender = healthyFish[1].convert()
                    elif angle <= .625*pi:
                        fishRender = healthyFish[2].convert()
                    elif angle <= .875*pi:
                        fishRender = healthyFish[3].convert()
                    elif angle <= 1.125*pi:
                        fishRender = healthyFish[4].convert()
                    elif angle <= 1.375*pi:
                        fishRender = healthyFish[5].convert()
                    elif angle <= 1.625*pi:
                        fishRender = healthyFish[6].convert()
                    else:
                        fishRender = healthyFish[7].convert()
                fishRender.convert()
                fishRender.set_alpha(255/(dist(fish.X,fish.Y,player.X,player.Y)/350 + 1))
                fishRender.set_colorkey((255,255,255))
                fishRender = transform.scale(fishRender,(round(7000/dist(fish.X,fish.Y,player.X,player.Y) + 1),round(7000//dist(fish.X,fish.Y,player.X,player.Y) + 1)))
                screen.blit(fishRender,(fish.xLocation - 3500/dist(fish.X,fish.Y,player.X,player.Y),350 - 3500/dist(fish.X,fish.Y,player.X,player.Y)))
    
    elif mode == PAUSE:
        mousePos = mouse.get_pos()
        mouse.set_visible(True)
        draw.rect(screen,(100,100,100),(150,150,400,400))
        draw.rect(screen,(0,0,200),menuButton1)
        draw.rect(screen,(200,0,0),menuButton2)
        if menuButton1.collidepoint(mousePos):
            draw.rect(screen,(0,0,255),menuButton1)
            if clicking:
                mode = GAME
        elif menuButton2.collidepoint(mousePos):
            draw.rect(screen,(255,0,0),menuButton2)
            if clicking:
                mode = MENU
        screen.blit(resumeText,(350-resumeWidth//2,305))
        screen.blit(mainMenuText,(350-mainMenuWidth//2,405))
    
    elif mode == INSTRUCTION:
        mousePos = mouse.get_pos()
        for x in range(0,601,100):
            screen.blit(background,(x,0))
        draw.rect(screen,(0,0,200),nextButton)
        draw.rect(screen,(0,0,200),backButton)
        screen.blit(instructions[instructionState],(50,50))        
        if nextButton.collidepoint(mousePos):
            draw.rect(screen,(0,0,255),nextButton)
            if clicking:
                if instructionState < 2:
                    instructionState += 1
                else:
                    instructionState = 0
                    mode = GAME
                    for fish in fishList:
                        fish.kill()
                        fish.countDown -= 300
                        player.alive = False
                        player.spawn(350,350)                    
        elif backButton.collidepoint(mousePos):
            draw.rect(screen,(0,0,255),backButton)
            if clicking:
                if instructionState > 0:
                    instructionState -= 1
                else:
                    mode = MENU
        screen.blit(backText,(100-backWidth//2,605))
        if instructionState < 2:
            screen.blit(nextText,(600-nextWidth//2,605))
        else:
            screen.blit(playText,(600-playWidth//2,605))
    
    clicking = False
    
    display.flip()
    clock.tick(60)

quit()