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
    if self.left_pressed:
      self.velX = -self.speed
    if self.right_pressed:
      self.velX = self.speed
    if self.up_pressed:
      self.velY = -self.speed
    if self.down_pressed:
      self.velY = self.speed
        
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

    # movement
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT and not snake.right_pressed:
          snake.left_pressed = True
          snake.up_pressed = False
          snake.down_pressed = False
      if event.key == pygame.K_RIGHT and not snake.left_pressed:
        snake.right_pressed = True
        snake.up_pressed = False
        snake.down_pressed = False
      if event.key == pygame.K_UP and not snake.down_pressed:
        snake.up_pressed = True
        snake.right_pressed = False
        snake.left_pressed = False
      if event.key == pygame.K_DOWN and not snake.up_pressed:
        snake.down_pressed = True
        snake.right_pressed = False
        snake.left_pressed = False
    if snake.x <= 0 and snake.left_pressed:
      gameStarted = False
      snake.left_pressed = False
      print("Game over")

  # giving the screen its colour
  screen.fill(background)

  # pressing a button will turn one of the boolean values to true
  if not gameStarted:
    screen.fill(background)
    if startButton.draw(screen):
      gameStarted = True

  if gameStarted:
      screen.fill(background)
      snake.draw(screen)
      

  snake.move()
  pygame.display.update()

pygame.quit()
