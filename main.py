import pygame

# button class
class Button():
    # constructor
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    # method to create the button on screen
    def draw(self, surface):
        action = False
        #getting mouse position
        pos = pygame.mouse.get_pos()

        #check if clicked or not
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        #drawing button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

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
startButton = Button(20, 10, startImg, 0.2)

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