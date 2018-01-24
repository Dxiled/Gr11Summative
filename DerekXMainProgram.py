'''''''''''''''''''''''''''''''''''''''''''''
Derek Xu
ICS3U1 Summative File
Main Program
Python version 3.6.1
'''''''''''''''''''''''''''''''''''''''''''''

from math import *              #Importing stuff
from random import *
from pygame import *
import os 
#Every module beyond here is of my own creation
from DerekXPlayerControl import *
from DerekXFishControl import *
from DerekXKeyFormulas import *
from DerekXGameMap import *
from DerekXBackgroundObjects import *

init()          #Setting up pygame and os window

os.environ['SDL_VIDEO_CENTERED'] = '1'

def drawBackground(window,player,image,stuff,up,left,down,right,sides,screenwidth):     #Function for drawing the background
    backgroundX = xLocation(player.angle,100*ceil(screenwidth/100))         #Calculates rotation of the background based on the player's angle
    backgroundX %= 100
    for x in range(-100,100*ceil(screenwidth/100),100):         #For loop draws the background (the background is a bunch of narrow, tilable textures)
        screen.blit(image,(x+backgroundX,0))
    for thing in stuff:             #If you're questioning the variable names, "stuff" represents stuff on the floor, and "thing" is each individual thing.
        thing.move(up,left,down,right,sides)        #Calls the method from the background class to move background things
    stuff.sort(key=lambda thing:thing.Y)            #Sorts the things by 'distance' (y-coordinate). lambda lets me sort a list of objects by one of their attributes.
    for thing in stuff:             #Draws the things in the list of things.
        thing.draw(window)

def drawHealth(window,health):      #Draws the hunger bar
    draw.rect(window,(255,0,0),(50,50,400,50))      #Draws a red rectangle for an empty bar
    draw.rect(window,(0,255,0),(50,50,health//5,50))    #"Fills" the bar with a green rectangle up to the player's health

def drawScore(window,score):        #Draws the current player score
    scoreString = "Score: " + str(score)    #Creates a string of text to display
    scoreRender = scoreFont.render(scoreString,False,(0,100,0))     #Renders said text with a font
    screen.blit(scoreRender,(650-scoreRender.get_width(),60))       #Displays text

def drawHighscore(window):          #Draws the current highscore onto the title page from the highscore file
    docR = open("DerekXHighscore.dat",'r')      #Opens the file 
    highscore = docR.readline()                 #Reads the number off
    docR.close()                                #Close
    highscoreRender = scoreFont.render("Highscore: " + highscore,False,(0,0,0))     #Renders the string with a font
    screen.blit(highscoreRender,(350 - highscoreRender.get_width()//2,200))         #Displays the text CENTERED under the title

screen = display.set_mode((700,700))    #Starts up the screen
clock = time.Clock()                    #Starts up a clock

player = playerControl()        #Initializes the player from the player class

fishList = []                   #
for count in range(10):         #Initializes ten fish from the fish class into a list
    buffer = fish()             #
    fishList.append(buffer)     #

running = True      #
w = False           #
a = False           #Initializes important booleans
s = False           #
d = False           #
clicking = False    #

#This gross pile of text imports the images into lists for easy access later.
background = image.load("DerekXBackground.png")
title = image.load("DerekXTitle.png")
healthyFish = [image.load("DerekXFish1Back.png"),image.load("DerekXFish1BackLeft.png"),image.load("DerekXFish1Left.png"),image.load("DerekXFish1FrontLeft.png"),image.load("DerekXFish1Front.png"),image.load("DerekXFish1FrontRight.png"),image.load("DerekXFish1Right.png"),image.load("DerekXFish1BackRight.png")]
unhealthyFish = [image.load("DerekXFish2Back.png"),image.load("DerekXFish2BackLeft.png"),image.load("DerekXFish2Left.png"),image.load("DerekXFish2FrontLeft.png"),image.load("DerekXFish2Front.png"),image.load("DerekXFish2FrontRight.png"),image.load("DerekXFish2Right.png"),image.load("DerekXFish2BackRight.png")]
instructions = [image.load("DerekXInstructions0.png"),image.load("DerekXInstructions1.png"),image.load("DerekXInstructions2.png"),image.load("DerekXInstructions3.png")]
biteList = [image.load("DerekXDolphinBite.png"),image.load("DerekXTurtleBite.png"),image.load("DerekXSharkBite.png")]

backgroundObjects = []                  #
for count in range(10):                 #Initializes ten background objects using the background class into a list
    buffer = bgObject()                 #
    backgroundObjects.append(buffer)    #

menuButton1 = Rect(200,300,300,50)      #
menuButton2 = Rect(200,400,300,50)      #
menuButton3 = Rect(200,500,300,50)      #Defines buttons for use in menus
backButton = Rect(50,600,100,50)        #
nextButton = Rect(550,600,100,50)       #

menuFont = font.SysFont("ocraii",40)    #
scoreFont = font.SysFont("ocraii",30)   #Initializes fonts
charFont = font.SysFont("ocraii",20)    #

playText = menuFont.render("Play",False,(0,0,100))                      #
instructionText = menuFont.render("How to Play",False,(0,0,100))        #
quitText = menuFont.render("Quit",False,(100,0,0))                      #
pausedText = menuFont.render("Paused",False,(0,0,0))                    #
resumeText = menuFont.render("Resume",False,(0,0,100))                  #
mainMenuText = menuFont.render("Main Menu",False,(100,0,0))             #Renders general text
nextText = menuFont.render("Next",False,(0,0,0))                        #
backText = menuFont.render("Back",False,(0,0,0))                        #
dolphinText = charFont.render("Dolphin (+speed)",False,(0,0,100))       #
turtleText = charFont.render("Turtle (-hunger)",False,(0,0,100))        #
sharkText = charFont.render("Shark (++speed,+hunger)",False,(0,0,100))  #

playWidth = playText.get_width()                    #
instructionWidth = instructionText.get_width()      #
quitWidth = quitText.get_width()                    #
pausedWidth = pausedText.get_width()                #Gets widths for most important text
resumeWidth = resumeText.get_width()                #
mainMenuWidth = mainMenuText.get_width()            #
nextWidth = nextText.get_width()                    #
backWidth = backText.get_width()                    #

instructionState = 0        #Initializes instructions controller

MENU = 0            #
GAME = 1            #
PAUSE = 2           #Modes
INSTRUCTION = 3     #
CHARSELECT = 4      #

mode = MENU         #Initializes mode variable

#Starts game loop
while running:
    for evnt in event.get():        #Gets all necessary input
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
                if mode == GAME:        #Shortcut here because ESC is only ever used to change modes
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
    
    if mode == MENU:        #Menu mode
        mouse.set_visible(True)         #Sets the cursor visible or else that would be bad
        for x in range(0,601,100):      #Draws a stationary background
            screen.blit(background,(x,0))
        screen.blit(title,(205,75))     #Draws the title block
        draw.rect(screen,(0,0,200),menuButton1)     #Draws the button
        draw.rect(screen,(0,0,200),menuButton2)
        draw.rect(screen,(200,0,0),menuButton3)
        mousePos = mouse.get_pos()
        if menuButton1.collidepoint(mousePos):      #Checks for mouseover the buttons and lights them up accordingly
            draw.rect(screen,(0,0,255),menuButton1)
            if clicking:            #On clicking play, prepares all entities and prompts user to choose a character
                mode = CHARSELECT
                for fish in fishList:
                    fish.kill()         #Resets fish
                    fish.countDown -= 300
                    player.alive = False    #Resets player
        elif menuButton2.collidepoint(mousePos):
            draw.rect(screen,(0,0,255),menuButton2)
            if clicking:
                mode = INSTRUCTION      #Takes the user to the instruction book
        elif menuButton3.collidepoint(mousePos):
            draw.rect(screen,(255,0,0),menuButton3)
            if clicking:
                running = False         #Exits the program
        drawHighscore(screen)           #Draws the highscore in the title block
        screen.blit(playText,(350-playWidth//2,305))                    #
        screen.blit(instructionText,(350-instructionWidth//2,405))      #Draws text on the buttons
        screen.blit(quitText,(350-quitWidth//2,505))                    #
    
    elif mode == GAME:
        mouse.set_visible(False)
        for fish in fishList:
            if not fish.alive:
                if fish.countDown == 0:
                    fish.spawn(player)      #Spawns a fish when its death timer expires
            
            fish.autoMove(player,[])        #Moves all fish using fish class
            fish.xLocation = xLocation(pi - polarAngle(player.X,player.Y,fish.X,fish.Y) + player.angle,700) + 350       #Number manipulation for pseudo-3D rendering
    
        if clicking:
            for fish in fishList:
                player.eat(fish)            #Attempts to eat every fish, only passes valid fish based on player class
        
        mouseMovement = (mouse.get_pos()[0] - 350,mouse.get_pos()[1] - 350)     #gets the degree of the mouses motion
        mouse.set_pos([350,350])        #Resets the mouse position to the middle so the mouseMovement will work again
        
        player.move(w,a,s,d,mouseMovement)      #Moves the player based on input
        player.get_health()                     #Tracks player's hunger bar
        if not player.alive:        #Detects the death
            mode = MENU
            docR = open("DerekXHighscore.dat",'r')      #Checks the highscore
            highscore = int(docR.readline())
            docR.close()
            if player.score > highscore:
                docW = open("DerekXHighscore.dat",'w')      #Updates the highscore if necessary
                docW.write(str(player.score))
                docW.close()

        drawBackground(screen,player,background,backgroundObjects,w,a,s,d,mouseMovement[0],700)     #Draws the dynamic background with off-screen shenannigans
        
        fishList.sort(key=lambda fish:fish.distance,reverse=True)       #Sorts the fish based on distance from the player (so back fish don't overlap front fish)
        for fish in fishList:
            if fish.alive:
                #This whole mess renders the fish so they face different directions
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
                fishRender = transform.scale(fishRender,(round(7000/(dist(fish.X,fish.Y,player.X,player.Y) + 1)),round(7000/(dist(fish.X,fish.Y,player.X,player.Y) + 1))))
                screen.blit(fishRender,(fish.xLocation - 3500/(dist(fish.X,fish.Y,player.X,player.Y) + 1),350 - 3500/(dist(fish.X,fish.Y,player.X,player.Y) + 1)))
                #Fish rendering stops here
        
        player.bite(screen,biteList)    #Biting animation
        
        #Draws the UI (health bar, score, cursor)
        drawHealth(screen,player.health)
        drawScore(screen,player.score)        
        draw.line(screen,(255,255,255),(325,350),(375,350),3)
        draw.line(screen,(255,255,255),(350,325),(350,375),3)
    
    elif mode == PAUSE:     #Pause menu (same as main menu but the buttons do different stuff)
        mousePos = mouse.get_pos()
        mouse.set_visible(True)
        draw.rect(screen,(100,100,100),(150,150,400,400))
        screen.blit(pausedText,(350-pausedWidth//2,200))
        draw.rect(screen,(0,0,200),menuButton1)
        draw.rect(screen,(200,0,0),menuButton2)
        if menuButton1.collidepoint(mousePos):
            draw.rect(screen,(0,0,255),menuButton1)
            if clicking:
                mode = GAME     #Resumes the game. Doesn't reset or change anything so the game is exactly how you left it.
        elif menuButton2.collidepoint(mousePos):
            draw.rect(screen,(255,0,0),menuButton2)
            if clicking:
                mode = MENU     #Quits to the main menu. This loses the current game because the main menu will overwrite it on 'play'
        screen.blit(resumeText,(350-resumeWidth//2,305))
        screen.blit(mainMenuText,(350-mainMenuWidth//2,405))
    
    elif mode == INSTRUCTION:       #Instructions book
        mousePos = mouse.get_pos()
        for x in range(0,601,100):
            screen.blit(background,(x,0))
        draw.rect(screen,(0,0,200),nextButton)      #Same idea as main menu but uses next and back buttons instead of menu buttons
        draw.rect(screen,(0,0,200),backButton)
        screen.blit(instructions[instructionState],(50,50))     #Displays the instruction page that corresponds with the counter        
        if nextButton.collidepoint(mousePos):
            draw.rect(screen,(0,0,255),nextButton)
            if clicking:
                if instructionState < 3:        #Next advances instruction counter
                    instructionState += 1
                else:
                    instructionState = 0        #If the counter won't advance further, resets it and mimics main menu's 'Play'
                    mode = CHARSELECT
                    for fish in fishList:
                        fish.kill()
                        fish.countDown -= 300
                        player.alive = False
        elif backButton.collidepoint(mousePos):
            draw.rect(screen,(0,0,255),backButton)
            if clicking:
                if instructionState > 0:        #Back button regresses instruction counter
                    instructionState -= 1
                else:
                    mode = MENU                 #If it won't regress further, takes the user back to the main menu
        screen.blit(backText,(100-backWidth//2,605))
        if instructionState < 3:
            screen.blit(nextText,(600-nextWidth//2,605))        #Chooses text for next button (last page is "Play" instead of "Next")
        else:
            screen.blit(playText,(600-playWidth//2,605))
    
    elif mode == CHARSELECT:
        mouse.set_visible(True)            #Reuses the main menu again
        for x in range(0,601,100):
            screen.blit(background,(x,0))
        draw.rect(screen,(0,0,200),menuButton1)
        draw.rect(screen,(0,0,200),menuButton2)
        draw.rect(screen,(0,0,200),menuButton3)
        mousePos = mouse.get_pos()
        #Spawns the player in as the desired character once selected
        if menuButton1.collidepoint(mousePos):
            draw.rect(screen,(0,0,255),menuButton1)
            if clicking:
                player.spawn(350,350,0)
                mode = GAME
        elif menuButton2.collidepoint(mousePos):
            draw.rect(screen,(0,0,255),menuButton2)
            if clicking:
                player.spawn(350,350,1)
                mode = GAME
        elif menuButton3.collidepoint(mousePos):
            draw.rect(screen,(0,0,255),menuButton3)
            if clicking:
                player.spawn(350,350,2)
                mode = GAME
        screen.blit(dolphinText,(350-dolphinText.get_width()//2,315))
        screen.blit(turtleText,(350-turtleText.get_width()//2,415))
        screen.blit(sharkText,(350-sharkText.get_width()//2,515))
    
    clicking = False        #Resets important variable
    
    display.flip()          #Animating
    clock.tick(60)

quit()