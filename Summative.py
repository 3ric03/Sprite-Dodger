import pygame
import random
import time

#Initialize Pygame
pygame.init()

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
plane = pygame.image.load("plane1.png")
background = pygame.image.load("p2.jpg")

#Create screen, caption and clock
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SPRITE DODGER v1.0")
clock = pygame.time.Clock()



#Functions

#Button function has two purposes
#It can write text to screen (called in draw section)
#It can return a Boolean if mouse click is on the word, allowing corresponding event to happen (called in events section)

def button (x, y, fontSize, txt, colour, mx=0, my=0, font = None):

    # Declare font, create text using provided text argument
    font = pygame.font.SysFont(font, fontSize)
    text = font.render(txt, True, colour)

    #Get coordinates of text rect for click dectection later
    fx, fy = text.get_rect().size
    screen.blit(text, (x,y))

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
    version = font2.render("Version 1.1 May 2019", True, red)
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
    music = ["music/Back On Track.mp3", "music/Dry Out.mp3", "music/Polargeist.mp3",
    "music/Base After Base.mp3", "music/Cycles.mp3"]
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

            #Play game button
            #This button can only be clicked when in the starting screen
            if not gameOver:

                #Check if button is pressed using the cursor positions aquired above
                if button(menuX + 200, menuY + 120, 50, "Play Game", blue, posX, posY):

                    #Switch on 'playing' to enter game mode
                    playing = True
                    #Switch off 'inMenu' to exit menu screen
                    inMenu = False
                

            #Quit game button
            if button(menuX + 260, menuY + 170, 50, "Quit", blue, posX, posY):

                #Break out of loop
                run = False

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
                move = 4

            #Left button pressed, negative move value (move left on x axis)
            elif event.key == pygame.K_LEFT:
                move = -4
                
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
            pygame.mixer.music.load("music/gameover.mp3")
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
quit()
