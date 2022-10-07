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

        # drawing button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

# snake class
class Snake:
  #constructor
  def __init__(self, x, y):
    self.x = int(x)
    self.y = int(y)
    self.rect = pygame.Rect(self.x, self.y, 32, 32)
    self.color = (120, 0, 120)
    self.velX = 0
    self.velY = 0
    self.left_pressed = False
    self.right_pressed = False
    self.up_pressed = False
    self.down_pressed = False
    self.speed = 1
      
  # draws snake on screen
  def draw(self, window):
    pygame.draw.rect(window, self.color, self.rect)

  # moving the snake
  def move(self):
    self.velX = 0
    self.velY = 0
    if not self.right_pressed:
      if self.left_pressed:
        self.velX = -self.speed
        self.up_pressed = False
        self.down_pressed = False
    if not self.left_pressed:
      if self.right_pressed:
        self.velX = self.speed
        self.up_pressed = False
        self.down_pressed = False
    if not self.down_pressed:
      if self.up_pressed:
        self.velY = -self.speed
        self.right_pressed = False
        self.left_pressed = False
    if not self.up_pressed:
      if self.down_pressed:
        self.velY = self.speed
        self.right_pressed = False
        self.left_pressed = False
        
    self.x += self.velX
    self.y += self.velY

    self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)


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

gameStarted = False
snake = Snake(screenWidth / 2, screenHeight / 2)

# creating gameplay loop
run = True
while run:
  for event in pygame.event.get():
    # ending the game when the window is closed
    if event.type == pygame.QUIT:
      run = False

    # checking what direction to move in
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        snake.left_pressed = True
      if event.key == pygame.K_RIGHT:
        snake.right_pressed = True
      if event.key == pygame.K_UP:
        snake.up_pressed = True
      if event.key == pygame.K_DOWN:
        snake.down_pressed = True

  # giving the screen its colour
  screen.fill(background)

  # pressing a button will turn one of the boolean values to true
  if startButton.draw(screen):
    gameStarted = True

  if gameStarted:
      screen.fill(background)
      snake.draw(screen)
      

  snake.move()
  pygame.display.update()

pygame.quit()
