import pygame
import button

pygame.init()

# giving the window its dimensions
screenWidth = 800
screenHeight = 700
screen = pygame.display.set_mode((screenWidth, screenHeight))

# giving the window a name
pygame.display.set_caption("Snek")

# making a colour for the background
background = (0, 200, 0)

# loading images from my computer into the program
startImg = pygame.image.load("start").convert_alpha()

# making a button using the image
startButton = button.Button(20, 10, startImg, 0.2)

# creating gameplay loop
run = True
while run:
    # giving the screen its colour
    screen.fill(background)

    # pressing a button will turn one of the boolean values to true
    if startButton.draw(screen):
        print("Clicked")

    # ending the game when the window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()