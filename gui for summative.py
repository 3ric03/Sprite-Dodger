#Summative

from tkinter import *
import pygame
import sys
from random import shuffle
from pygame.locals import *
import random
import time

colour = (255,255,255)

screen = Tk()
screen.title("Pygame Arcade")
screen.geometry("380x200")

myFont = "Hevetica 12 bold"

##########################

def game1():
    space()

def game2():
    Eric1()

##########################

#Select game
Label(screen, text = "Select a game: ", fg = "blue", font = myFont).grid(row = 0, column = 1)

#Game button
Button(screen, text = "Space Invaders!", width = 20, bg = "green", fg = "white", font = myFont, command = game1).grid(row = 1, column= 1, pady = 10)
Button(screen, text = "Sprite Dodger!", width = 20, bg = "green", fg = "white", font = myFont, command = game2).grid(row = 2, column = 1, pady = 10)

#Space Invaders

def space():

##Space Invaders##

    ##CONSTANTS##

    ## COLORS ##

    #            R    G    B
    GRAY      = (100, 100, 100)
    NAVYBLUE  = ( 60,  60, 100)
    WHITE     = (255, 255, 255)
    RED       = (255,   0,   0)
    GREEN     = (  0, 255,   0)
    BLUE      = (  0,   0, 255)
    YELLOW    = (255, 255,   0)
    ORANGE    = (255, 128,   0)
    PURPLE    = (255,   0, 255)
    CYAN      = (  0, 255, 255)
    BLACK     = (  0,   0,   0)
    NEARBLACK = ( 19,  15,  48)
    COMBLUE   = (233, 232, 255)

    ## Background Music ##
    
    pygame.mixer.init()
    pygame.mixer.music.load("ogg/Avengers Theme.ogg")
    pygame.mixer.music.set_volume(2)
    pygame.mixer.music.play(-1)
    
    ## Player Constants ##

    PLAYERWIDTH = 4
    PLAYERHEIGHT = 10
    PLAYERCOLOR = COMBLUE
    PLAYER1 = 'Player 1'
    PLAYERSPEED = 5
    PLAYERCOLOR = GREEN

    ## Display Constants ##

    GAMETITLE = 'Avengers: Invaders!'
    DISPLAYWIDTH = 640
    DISPLAYHEIGHT = 480
    BGCOLOR = NEARBLACK
    XMARGIN = 50
    YMARGIN = 50

    ## Bullet Constants ##

    BULLETWIDTH = 5
    BULLETHEIGHT = 5
    BULLETOFFSET = 700

    ## Enemy Constants ##


    ENEMYWIDTH = 25
    ENEMYHEIGHT = 25
    ENEMYNAME = 'Enemy'
    ENEMYGAP = 20
    ARRAYWIDTH = 10
    ARRAYHEIGHT = 4
    MOVETIME = 1000
    MOVEX = 10
    MOVEY = ENEMYHEIGHT
    TIMEOFFSET = 300


    ## This dictionary allows for shooting bullets while moving without ##
    ## the inputs interupting each other.                               ##

    DIRECT_DICT = {pygame.K_LEFT  : (-1),
                   pygame.K_RIGHT : (1)}





    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.width = PLAYERWIDTH
            self.height = PLAYERHEIGHT
            self.image = pygame.image.load("images/summative_thanos.png").convert_alpha()
            self.color = PLAYERCOLOR
            self.rect = self.image.get_rect()
            self.name = PLAYER1
            self.speed = PLAYERSPEED
            self.vectorx = 0

        
        def update(self, keys, *args):
            for key in DIRECT_DICT:
                if keys[key]:
                    self.rect.x += DIRECT_DICT[key] * self.speed
                    
            self.checkForSide()


        def checkForSide(self):
            if self.rect.right > DISPLAYWIDTH:
                self.rect.right = DISPLAYWIDTH
                self.vectorx = 0
            elif self.rect.left < 0:
                self.rect.left = 0
                self.vectorx = 0



    class Blocker(pygame.sprite.Sprite):
        def __init__(self, side, color, row, column):
            pygame.sprite.Sprite.__init__(self)
            self.width = side
            self.height = side
            self.color = color
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(self.color)
            self.rect = self.image.get_rect()
            self.name = 'blocker'
            self.row = row
            self.column = column



    class Bullet(pygame.sprite.Sprite):
        def __init__(self, rect, color, vectory, speed):
            pygame.sprite.Sprite.__init__(self)
            self.width = BULLETWIDTH
            self.height = BULLETHEIGHT
            self.color = color
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(self.color)
            self.rect = self.image.get_rect()
            self.rect.centerx = rect.centerx
            self.rect.top = rect.bottom
            self.name = 'bullet'
            self.vectory = vectory
            self.speed = speed
        

        def update(self, *args):
            self.oldLocation = (self.rect.x, self.rect.y)
            self.rect.y += self.vectory * self.speed

            if self.rect.bottom < 0:
                self.kill()

            elif self.rect.bottom > 500:
                self.kill()

            

    class Enemy(pygame.sprite.Sprite):
        
        def __init__(self, row, column):
            pygame.sprite.Sprite.__init__(self)
            self.width = ENEMYWIDTH
            self.height = ENEMYHEIGHT
            self.row = row
            self.column = column
            self.image = self.setImage()
            self.rect = self.image.get_rect()
            self.name = 'enemy'
            self.vectorx = 1
            self.moveNumber = 0
            self.moveTime = MOVETIME
            self.timeOffset = row * TIMEOFFSET
            self.timer = pygame.time.get_ticks() - self.timeOffset


        def update(self, keys, currentTime):
            if currentTime - self.timer > self.moveTime:
                if self.moveNumber < 6:
                    self.rect.x += MOVEX * self.vectorx
                    self.moveNumber += 1
                elif self.moveNumber >= 6:
                    self.vectorx *= -1
                    self.moveNumber = 0
                    self.rect.y += MOVEY
                    if self.moveTime > 100:
                        self.moveTime -= 50
                self.timer = currentTime


        def setImage(self):
            if self.row == 0:
                image = pygame.image.load('images/alien1.png')
            elif self.row == 1:
                image = pygame.image.load('images/alien2.png')
            elif self.row == 2:
                image = pygame.image.load('images/alien3.png')
            else:
                image = pygame.image.load('images/alien1.png')
            image.convert_alpha()
            image = pygame.transform.scale(image, (self.width, self.height))

            return image




    class Text(object):
        def __init__(self, font, size, message, color, rect, surface):
            self.font = pygame.font.Font(font, size)
            self.message = message
            self.surface = self.font.render(self.message, True, color)
            self.rect = self.surface.get_rect()
            self.setRect(rect)

        def setRect(self, rect):
            self.rect.centerx, self.rect.centery = rect.centerx, rect.centery - 5


        def draw(self, surface):
            surface.blit(self.surface, self.rect)



    class App(object):
        
        def __init__(self):
            pygame.init()
            self.displaySurf, self.displayRect = self.makeScreen()
            self.gameStart = True
            self.gameOver = False
            self.beginGame = False
            self.laserSound = pygame.mixer.Sound('ogg/laser.ogg')
            self.startLaser = pygame.mixer.Sound('ogg/alienLaser.ogg')



        def resetGame(self):
            self.gameStart = True
            self.needToMakeEnemies = True
            
            self.introMessage1 = Text('orena.ttf', 25,
                                     'Welcome to  Avengers: Invaders!',
                                     GREEN, self.displayRect,
                                     self.displaySurf)
            self.introMessage2 = Text('orena.ttf', 20,
                                      'Press Any Key to Continue',
                                      GREEN, self.displayRect,
                                      self.displaySurf)
            self.introMessage2.rect.top = self.introMessage1.rect.bottom + 5

            self.gameOverMessage = Text('orena.ttf', 25,
                                        'GAME OVER', GREEN,
                                        self.displayRect, self.displaySurf)
            
            self.player = self.makePlayer()
            self.bullets = pygame.sprite.Group()
            self.greenBullets = pygame.sprite.Group()
            self.blockerGroup1 = self.makeBlockers(0)
            self.blockerGroup2 = self.makeBlockers(1)
            self.blockerGroup3 = self.makeBlockers(2)
            self.blockerGroup4 = self.makeBlockers(3)
            self.allBlockers = pygame.sprite.Group(self.blockerGroup1, self.blockerGroup2,
                                                   self.blockerGroup3, self.blockerGroup4)
            self.allSprites = pygame.sprite.Group(self.player, self.allBlockers)
            self.keys = pygame.key.get_pressed()
            self.clock = pygame.time.Clock()
            self.fps = 60
            self.enemyMoves = 0
            self.enemyBulletTimer = pygame.time.get_ticks()
            self.gameOver = False
            self.gameOverTime = pygame.time.get_ticks()

            



        def makeBlockers(self, number=1):
            blockerGroup = pygame.sprite.Group()
            
            for row in range(5):
                for column in range(7):
                    blocker = Blocker(10, GREEN, row, column)
                    blocker.rect.x = 50 + (150 * number) + (column * blocker.width)
                    blocker.rect.y = 375 + (row * blocker.height)
                    blockerGroup.add(blocker)

            for blocker in blockerGroup:
                if (blocker.column == 0 and blocker.row == 0
                    or blocker.column == 6 and blocker.row == 0):
                    blocker.kill()

            return blockerGroup



        def checkForEnemyBullets(self):
            redBulletsGroup = pygame.sprite.Group()

            for bullet in self.bullets:
                if bullet.color == RED:
                    redBulletsGroup.add(bullet)

            for bullet in redBulletsGroup:
                if pygame.sprite.collide_rect(bullet, self.player):
                    if self.player.color == GREEN:
                        self.player.color = YELLOW
                    elif self.player.color == YELLOW:
                        self.player.color = RED
                    elif self.player.color == RED:
                        self.gameOver = True
                        self.gameOverTime = pygame.time.get_ticks()
                    bullet.kill()



        def shootEnemyBullet(self, rect):
            if (pygame.time.get_ticks() - self.enemyBulletTimer) > BULLETOFFSET:
                self.bullets.add(Bullet(rect, RED, 1, 5))
                self.allSprites.add(self.bullets)
                self.enemyBulletTimer = pygame.time.get_ticks()



        def findEnemyShooter(self):
            columnList = []
            for enemy in self.enemies:
                columnList.append(enemy.column)

            #get rid of duplicate columns
            columnSet = set(columnList)
            columnList = list(columnSet)
            shuffle(columnList)
            column = columnList[0]
            enemyList = []
            rowList = []

            for enemy in self.enemies:
                if enemy.column == column:
                    rowList.append(enemy.row)

            row = max(rowList)

            for enemy in self.enemies:
                if enemy.column == column and enemy.row == row:
                    self.shooter = enemy 

            
            
            
            
        

        def makeScreen(self):
            pygame.display.set_caption(GAMETITLE)
            displaySurf = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
            displayRect = displaySurf.get_rect()
            displaySurf.fill(BGCOLOR)
            displaySurf.convert()

            return displaySurf, displayRect



        def makePlayer(self):
            player = Player()
            ##Place the player centerx and five pixels from the bottom
            player.rect.centerx = self.displayRect.centerx
            player.rect.bottom = self.displayRect.bottom - 5

            return player



        def makeEnemies(self):
            enemies = pygame.sprite.Group()
            
            for row in range(ARRAYHEIGHT):
                for column in range(ARRAYWIDTH):
                    enemy = Enemy(row, column)
                    enemy.rect.x = XMARGIN + (column * (ENEMYWIDTH + ENEMYGAP))
                    enemy.rect.y = YMARGIN + (row * (ENEMYHEIGHT + ENEMYGAP))
                    enemies.add(enemy)

            return enemies



        def checkInput(self):
            for event in pygame.event.get():
                self.keys = pygame.key.get_pressed()
                if event.type == QUIT:
                    self.terminate()

                elif event.type == KEYDOWN:
                    if event.key == K_SPACE and len(self.greenBullets) < 1:
                        bullet = Bullet(self.player.rect, GREEN, -1, 20)
                        self.greenBullets.add(bullet)
                        self.bullets.add(self.greenBullets)
                        self.allSprites.add(self.bullets)
                    elif event.key == K_ESCAPE:
                        self.terminate()


        def gameStartInput(self):
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYUP:
                    self.gameOver = False
                    self.gameStart = False
                    self.beginGame = True


        def gameOverInput(self):
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYUP:
                    self.gameStart = True
                    self.beginGame = False
                    self.gameOver = False
        

            


        def checkCollisions(self):
            self.checkForEnemyBullets()
            pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
            pygame.sprite.groupcollide(self.enemies, self.allBlockers, False, True)
            self.collide_green_blockers()
            self.collide_red_blockers()
            

            
        def collide_green_blockers(self):
            for bullet in self.greenBullets:
                casting = Bullet(self.player.rect, GREEN, -1, 20)
                casting.rect = bullet.rect.copy()
                for pixel in range(bullet.speed):
                    hit = pygame.sprite.spritecollideany(casting,self.allBlockers)
                    if hit:
                        hit.kill()
                        bullet.kill()
                        break
                    casting.rect.y -= 1


        def collide_red_blockers(self):
            reds = (shot for shot in self.bullets if shot.color == RED)
            red_bullets = pygame.sprite.Group(reds)
            pygame.sprite.groupcollide(red_bullets, self.allBlockers, True, True)

        



        def checkGameOver(self):
            if len(self.enemies) == 0:
                self.gameOver = True
                self.gameStart = False
                self.beginGame = False
                self.gameOverTime = pygame.time.get_ticks()

            else:
                for enemy in self.enemies:
                    if enemy.rect.bottom > DISPLAYHEIGHT:
                        self.gameOver = True
                        self.gameStart = False
                        self.beginGame = False
                        self.gameOverTime = pygame.time.get_ticks()
           
            
                    

        def terminate(self):
            pygame.quit()
            sys.exit()


        def mainLoop(self):
            while True:
                if self.gameStart:
                    self.resetGame()
                    self.gameOver = False
                    self.displaySurf.fill(BGCOLOR)
                    self.introMessage1.draw(self.displaySurf)
                    self.introMessage2.draw(self.displaySurf)
                    self.gameStartInput()
                    pygame.display.update()

                elif self.gameOver:
                    self.displaySurf.fill(BGCOLOR)
                    self.gameOverMessage.draw(self.displaySurf)
                    #prevent users from exiting the GAME OVER screen
                    #too quickly
                    if (pygame.time.get_ticks() - self.gameOverTime) > 2000:
                        self.gameOverInput()
                    pygame.display.update()
                    
                elif self.beginGame:
                    if self.needToMakeEnemies:
                        
                        self.enemies = self.makeEnemies()
                        self.allSprites.add(self.enemies)
                        self.needToMakeEnemies = False
                        pygame.event.clear()
                        
                        
                            
                    else:    
                        currentTime = pygame.time.get_ticks()
                        self.displaySurf.fill(BGCOLOR)
                        self.checkInput()
                        self.allSprites.update(self.keys, currentTime)
                        if len(self.enemies) > 0:
                            self.findEnemyShooter()
                            self.shootEnemyBullet(self.shooter.rect)
                        self.checkCollisions()
                        self.allSprites.draw(self.displaySurf)
                        self.blockerGroup1.draw(self.displaySurf)
                        pygame.display.update()
                        self.checkGameOver()
                        self.clock.tick(self.fps)
                        
                
                
        


    if __name__ == '__main__':
        app = App()
        app.mainLoop()


def Eric1():
    pygame.init()
    global colour

        #Declare constants
    size = (width, height) = (1200, 600)

    white = (255, 255, 255)
    red = (255, 0 ,0)
    green = (0, 255,0)
    blue = (0, 0, 255)
    black=(0,0,0)
    yellow = (255, 255, 0)
    screenColour = (46, 7, 136)
    scoreColour = (9, 243, 227)

    blockColours = [red, (255, 127, 0), yellow, (127, 255, 0), green,
                    (0, 255, 127), (0, 255, 255), (0, 127, 255), blue, (127, 0, 255), (255, 0, 255), (255, 0, 127)]

    colour = red
    score = 0
    heightX, heightY, heightZ  = 0, 0, 0
    pX = 560
    pY = 400
    speed = 2
    move = 0
    menuX, menuY = 300, 110

    #Create font
    font = pygame.font.Font(None, 40)

    #boolean var declaration
    
    inMenu = True
    playing = False
    gameOver = False                                     
    
    generate = True
    firstRun = True
    Ygen = False
    Zgen = False
    first = True
    colourChanger = False
    collided = False



    #Load images
    plane = pygame.image.load("images/plane1.png")
    background = pygame.image.load("images/p2.jpg")

    #Create screen, caption and clock
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("SPRITE DODGER v1.1")
    clock = pygame.time.Clock()



    #Functions

    #Button function has two purposes
    #It can write text to screen (called in draw section)
    #It can return a Boolean if mouse click is on the word, allowing corresponding event to happen (called in events section)

    def button (x, y, fontSize, txt, colour, mx=0, my=0, font = None):

        # Declare font, create text using provided text argument
        font = pygame.font.SysFont(font, fontSize)
        text = font.render(txt, True, colour)

        screen.blit(text, (x,y))

        
        #Get coordinates of text rect for click dectection later
        fx, fy = text.get_rect().size
        
        #If mouse coordinates during the click (mx, my) is inside rect, return True
        if pygame.Rect(x,y,fx,fy).collidepoint(mx, my):
            return True

    #Function to change colour of obstacles
    #Argument is y value of obastacle
    def colourChange(y):

        #Modify the colour variable globally so it can be applied in the draw section
        global colour
        #local variable changed to control rate of change
        changed = False

        #When y is a number divisible by 100 and colour has not changed
        if y % 100 == 0 and not changed:

            #Change a colour to a random one in the list
            colour = random.choice(blockColours)
            #changed boolean is True so colour won't be changed again
            changed = True

        #If statement to change boolean to false so colour change will take place
        if (y + 2) % 2 == 0:
            changed = False

    #Create a rectangular surface (obstacle) with given value
    def blockMaker(x, length, colour, dropValue):
        surface = pygame.Rect(x, -50 + dropValue, length, 30)
        return surface

    #Generates the dimensions (length and cordinates) of a row of obstacle (3)
    def generator():

        #Generate length for all 3 rect
        length1 = random.randint(200, 300)
        length2 = random.randint(200, 300)
        length3 = random.randint(200, 300)

        #Generate x cord for three rect
        a = random.randint(0, 300)
        b = random.randint(a + 400, a + 500)
        c = random.randint(b + 400, b + 500)

        return length1, length2, length3, a, b, c
            

    #Function that displays menu screen
    def menu(x, y):
        
        #Create font and menu text
        font = pygame.font.SysFont('rockwell', 80)
        title = font.render("SPRITE DODGER", True, red)
        font2 = pygame.font.SysFont('rockwell', 20)
        version = font2.render("Version 1.1 June 2019", True, red)
        font3 = pygame.font.SysFont('rockwell', 25)
        instruction = font3.render("Dodge obstacles with your airplane using arrow keys", True, white)

        #Blit text
        screen.blit(background, (0,0))
        screen.blit(title, (x, y))
        screen.blit(version, (x + 350, y + 80))
        screen.blit(instruction, ((x + 20, y + 330)))

        #Call on button function to create 'Play Game' and 'Quit' buttons
        button(x + 220, y + 120, 50, "Play Game", green)
        button(x + 260, y + 170, 50, "Quit", green)

    #Function that displays the gameover screen
    def restartMenu(x, y, score, highScore):

        #Create font and text
        font = pygame.font.Font('freesansbold.ttf', 50)
        score = font.render("Your Score: " + str(score), True, red)
        highScore = font.render("High score: " + str(highScore), True, red)

        #Blit text
        screen.blit(score, (x + 100, y))
        screen.blit(highScore, (x + 105, y + 50))

        # #Call on button function to create 'Play Again' and 'Quit' buttons
        button(x + 220, y + 120, 50, "Play Again", green)
        button(x + 260, y + 170, 50, "Quit", green)

    #Function to log current score and track high score through txt file
    #Take most recent score as argument
    def scoreKeeper(score):

        #list for score sorting
        data = []

        #Open scorekeeping txt in append mode
        with open('Scores.txt', 'a') as file:

            #Add most recent score
            file.write(str(score) + '\n')

        #Open scorekeeping txt in reading mode
        with open('Scores.txt', 'r') as file1:

            #Add all data into a list as integers
            for thing in file1:
                thing = thing.strip()
                data.append(int(thing))

            #Get highest score
            highScore = max(data)

        return highScore

    #Function to play music
    def music():

        #Pick a random soundtrack out of the five given eveytime the game starts
        pygame.mixer.init()
        music = ["Back On Track.mp3", "Dry Out.mp3", "Polargeist.mp3","Base After Base.mp3", "Cycles.mp3"]
        pygame.mixer.music.load(random.choice(music))
        pygame.mixer.music.play(1)


    #Main game loop
    run = True

    while run:
        #event section
        for event in pygame.event.get():

            #Get mouse event
            mouse_pressed = pygame.mouse.get_pressed()

            #Close window
            if event.type == pygame.QUIT:
                run = False

            #Event: Mouse left button click
            if mouse_pressed[0]:
                
                #Get current cursor position 
                posX, posY = pygame.mouse.get_pos()

                #Quit game button
                if button(menuX + 260, menuY + 170, 50, "Quit", blue, posX, posY):

                    #Break out of loop
                    run = False

                #Play game button
                #This button can only be clicked when in the starting screen
                if not gameOver:

                    #Check if button is pressed using the cursor positions aquired above
                    if button(menuX + 200, menuY + 120, 50, "Play Game", blue, posX, posY):

                        #Switch on 'playing' to enter game mode
                        playing = True
                        #Switch off 'inMenu' to exit menu screen
                        inMenu = False

                #Restart button
                if button(menuX + 200, menuY + 120, 50, "Play Again", blue, posX, posY):

                    #Reset variables for the next run
                    playing = True
                    gameover = False
                    firstRun = True
                    first = True
                    heightX = 0
                    heightY = 0
                    score = 0
                    heightZ = 0
                    Ygen = False
                    Zgen = False
                    collided = False
                    pX = 560
                    

            #Event: Key down
            elif event.type == pygame.KEYDOWN:

                #Right keep pressed, positive move value (move right on x axis)
                if event.key == pygame.K_RIGHT:
                    move = 2

                #Left button pressed, negative move value (move left on x axis)
                elif event.key == pygame.K_LEFT:
                    move = -2
                    
            #Event: User lets go of key
            elif event.type == pygame.KEYUP:

                #When user let go of either key, move value is zero, so aeroplane stops moving
                if event.key == pygame.K_RIGHT :
                    move = 0
        
                elif event.key == pygame.K_LEFT:
                    move = 0
                    
        #game logic
        if playing:
            

            #Check if aeroplane icon will be out of bounds, if so, movement value is zero to stop moving
            if pX + move < 0 or pX + move > 1120:
                move = 0

            #Add move value to X position to move (or stop moving)
            pX += move

            #Put aeroplane icon on screen
            p = screen.blit(plane, (pX,pY))

            #render score text
            scoreTxt = font.render("SCORE:" + str(score), True, scoreColour)
            
            #If it's very first run, play music and generate values for obstacle row A
            if firstRun:
                music()
                
                LX1, LX2, LX3, aX, bX, cX = generator()
                LY1, LY2, LY3, aY, bY, cY = generator()
                LZ1, LZ2, LZ3, aZ, bZ, cZ = generator()

                #First run actions complete, therefore no longer first run
                firstRun = False


            
            #Create surfaces of rects in obstacle row A 
            r1s1 = blockMaker(aX, LX1, colour, heightX)
            r1s2 = blockMaker(bX, LX2, colour, heightX)
            r1s3 = blockMaker(cX, LX3, colour, heightX)

            #Change y values of obstacle row A so it moves downward
            heightX += speed

            #Check for collision with any objects in row A
            if r1s1.colliderect(p) or r1s2.colliderect(p) or r1s3.colliderect(p):
                collided = True

            #Conditions to check if row A has moved off screen and needs to respawn on top
            if heightX == 640 and heightY > 600:
                heightX = 0
                #Generate new coordinates and values for next spawn
                LX1, LX2, LX3, aX, bX, cX = generator()
           
            #When row A halfway across screen, generate row B
            if heightX >= 300:
                Ygen = True
                
            #SAME CONCEPT AS ROW A, JUST DIFFERENT VARIABLES
            if Ygen:
                r2s1 = blockMaker(aY, LY1, colour, heightY)
                r2s2 = blockMaker(bY, LY2, colour, heightY)
                r2s3 = blockMaker(cY, LY3, colour, heightY)
            
                heightY += speed

                if r2s1.colliderect(p) or r2s2.colliderect(p) or r2s3.colliderect(p):
                    collided = True
     
                if heightY == 640:
                    heightY = 0
                    LY1, LY2, LY3, aY, bY, cY = generator()

            #When row A off screen, generate row C
            if heightX >= 600:
                Zgen = True
                
            #SAME CONCEPT AS ROW A, JUST DIFFERENT VARIABLES
            if Zgen:
                r3s1 = blockMaker(aZ, LZ1, colour, heightZ)
                r3s2 = blockMaker(bZ, LZ2, colour, heightZ)
                r3s3 = blockMaker(cZ, LZ3, colour, heightZ)

                if r3s1.colliderect(p) or r3s2.colliderect(p) or r3s3.colliderect(p):
                    collided = True

            
                heightZ += speed
                
                if heightZ == 640:
                    heightZ = 0
                    LZ1, LZ2, LZ3, aZ, bZ, cZ = generator()

            #Increase score   
            score += 1

            
            #If collision occurs
            if collided:
                
                #Change boolean to change mode
                playing = False
                gameover = True

                
                #Stop gameplay music and play gameover music ONCE
                pygame.mixer.music.stop()
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play(1)

            #Colour changer
            if colourChanger:
                colourChange(heightX)
                


        #drawing

        #fill background
        screen.fill(screenColour)

        #run menu function if in menu
        if inMenu:
            menu(menuX, menuY)
            

        elif playing:
            
            #while score < 600, obstacle colour is red
            if score < 600:
                colour = red

            #if higher, change boolean to turn on random colour change function 
            else:
                colourChanger = True
                

            #Draw obstacle row A
            pygame.draw.rect(screen, colour, r1s1)
            pygame.draw.rect(screen, colour, r1s2)
            pygame.draw.rect(screen, colour, r1s3)

            #Draw row B and C when they are generated
            if Ygen:
                pygame.draw.rect(screen, colour, r2s1)
                pygame.draw.rect(screen, colour, r2s2)
                pygame.draw.rect(screen, colour, r2s3)

            if Zgen:
                pygame.draw.rect(screen, colour, r3s1)
                pygame.draw.rect(screen, colour, r3s2)
                pygame.draw.rect(screen, colour, r3s3)


            #Draw bjects
            screen.blit(plane, (pX,pY))
            screen.blit(scoreTxt, (0,10))
            
        elif gameover:

            #First time this runs
            if first:

                #use function to log score
                highScore = (scoreKeeper(score))
                first = False

            #Display gameover menu
            restartMenu(menuX, menuY, score, highScore)
        
        pygame.display.flip()

        #Change frame rate to increase speeed of obstacle movement based on score
        if score < 600:
            clock.tick(120)
        elif score < 4000:
            clock.tick(240)
        else:
            clock.tick(300)


    pygame.quit()





screen.mainloop()
