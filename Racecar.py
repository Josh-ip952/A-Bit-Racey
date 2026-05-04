import pygame
import time
import random

#######################################################################################
# Following code from https://pythonprogramming.net/pygame-start-menu-tutorial/
# Some parts are refactored
# Comments are added, there were no comments in the original code
#######################################################################################


pygame.init()
pygame.mixer.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
block_color = (53, 115, 255)

# Car width is dependent on the image input
car_width = 73

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

carImg = pygame.image.load('./racecar.png')

# Add sound effects
music = pygame.mixer.music.load('Tobu - Candyland.mp3')
crash_sound = pygame.mixer.Sound(
    'dragon-studio-car-crash-sound-effect-376874.mp3')


# Count how many objects are dodged
def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text, (0, 0))

# Draw the obstacles (rectangles) based on random generations input into this function


def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

# Car is on the coordinates (x,y), which changes whenever user moves the car


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

# Display a large text that appears for a certain time period


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 100)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


# Button function below is from
# https://github.com/detnsw-sydtech/depth-first-search-algorithm-tutorial
# Author: Asati, C

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    # print(mouse)
    click = pygame.mouse.get_pressed()
    # print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            pygame.time.delay(200)
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf, textRect)


# Crash function below is from
# https://github.com/detnsw-sydtech/depth-first-search-algorithm-tutorial
# Author: Asati, C

def crash():
    pygame.mixer.Sound.play(crash_sound)
    crash_sound.set_volume(0.35)
    pygame.mixer.music.stop()  # Stop background music
    
    while True:

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                endgame()
 
        gameDisplay.fill(white)

        message_display('You Crashed')

        button("Play Again", 150, 450, 150, 50, green, green, game_loop)
        button("Quit", 550, 450, 100, 50, red, red, endgame)

        pygame.display.update()
        clock.tick(60)
        


# The game_intro function is refactored
# Starting menu is edited

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                endgame()

            # Add function: game starts when player presses space bar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

        gameDisplay.fill(white)

        # Assign font
        largeText = pygame.font.Font('freesansbold.ttf', 100)
        normalText = pygame.font.Font('freesansbold.ttf', 48)

        # Create Title
        TitleSurf, TitleRect = text_objects("A Bit Racey", largeText)
        TitleRect.center = ((display_width/2), (display_height/2) - 50)
        gameDisplay.blit(TitleSurf, TitleRect)

        # Create instructions to start the game
        TextSurf, TextRect = text_objects(
            "Press Space Bar To Play!", normalText)
        TextRect.center = ((display_width/2), (display_height/2) + 100)
        gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(15)


def endgame():
    pygame.quit()
    quit()


def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100

    thingCount = 1

    dodged = 0

    gameExit = False

    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endgame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)

        things(thing_startx, thing_starty,
               thing_width, thing_height, block_color)

        thing_starty += thing_speed
        car(x, y)
        things_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)

        if y < thing_starty+thing_height:
            print('y crossover')

            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                print('x crossover')
                crash()

        pygame.display.update()
        clock.tick(60)


game_intro()
game_loop()
endgame()
