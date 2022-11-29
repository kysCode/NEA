import pygame, random
from pygame.math import Vector2

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
    # getting mouse position
    pos = pygame.mouse.get_pos()

    # check if clicked or not
    if self.rect.collidepoint(pos):
      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
        self.clicked = True
        action = True

    # drawing button on screen
    surface.blit(self.image, (self.rect.x, self.rect.y))

    return action


# snake class
class Snake():
  # constructor
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.body = [Vector2(x, y), Vector2(x - 23, y), (x - 46, y)]
    self.rect = pygame.Rect(self.x, self.y, 32, 32)
    self.velX = 0
    self.velY = 0
    self.left_pressed = False
    self.right_pressed = False
    self.up_pressed = False
    self.down_pressed = False
    self.vector = Vector2(0,0)
    self.hitBoundary = False
    self.angle = 0
    self.score = 0

  # draws snake on screen
  def draw(self, window):
    for block in self.body:
      block_rect = pygame.Rect(block[0], block[1], 23, 23)
      pygame.draw.rect(screen,(128,0,128), block_rect)

  # moving the snake
  def move(self):
    # checking if the snake has hit the edge of the screen
    if not (self.body[0][0] > 0 and self.body[0][0] < 777 and self.body[0][1] > 0 and self.body[0][1] < 628):
      self.hitBoundary = True
      self.vector = (0,0)

    else:
      # creating the vector which is used to move the snake
      if self.left_pressed:
        self.vector = Vector2(-1, 0)
        self.turning_point = (self.x + 23, self.y)
      if self.right_pressed:
        self.vector = Vector2(1, 0)
      if self.up_pressed:
        self.vector = Vector2(0, -1)
      if self.down_pressed:
        self.vector = Vector2(0, 1)

    body_copy = self.body[:-1] # copies all the items in the body apart from the last one
    body_copy.insert(0, body_copy[0] + self.vector) # inserts a new head at the new position
    self.body = body_copy[:] # contents are copied back into the original

# fruit class
class Fruit():
  # constructor
  def __init__(self, image):
    self.image = pygame.transform.scale(image, (35, 35))
    self.x = -1
    self.y = -1
    self.drawn = False

  # assigning the fruit to a location
  def randomiseLocation(self, w, h):
    if not self.drawn:
      self.x = random.randint(0, w - 22)
      self.y = random.randint(0, h - 22)

  # drawing the fruit on the screen
  def draw(self, width, height, window):
    self.randomiseLocation(width, height)
    window.blit(self.image, (self.x, self.y))
    self.drawn = True


pygame.init()

# creating text font and colour
font = pygame.font.SysFont('Arial', 24)
black = (0, 0, 0)

# giving the window its dimensions
screenWidth = 800
screenHeight = 650
screen = pygame.display.set_mode((screenWidth, screenHeight))

# giving the window a name
pygame.display.set_caption("Snek")

# making a colour for the background
background = (0, 175, 0)

# loading images from computer into the program
startImg = pygame.image.load("start").convert_alpha()
snakeHead = pygame.image.load("snakeHead.png").convert_alpha()
snakeBody = pygame.image.load("snakeBody.png").convert_alpha()
snakeEnd = pygame.image.load("snakeEnd.png").convert_alpha()
fruitImg = pygame.image.load("fruit.png").convert_alpha()

# making a button using the image
startButton = Button(20, 10, startImg, 0.2)

gameStarted = False
gameOver = False
snake = Snake(screenWidth / 2, screenHeight / 2)
apple = Fruit(fruitImg)

# creating gameplay loop
run = True
while run:
  score = font.render(("Score: " + str(snake.score)), True, black, background)
  for event in pygame.event.get():
    # ending the game when the window is closed
    if event.type == pygame.QUIT:
        run = False

    # changing the direction of movement depending on the key that was pressed
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

    # ending the game when the snake hits the edge
    if snake.hitBoundary and not gameOver:
      print("Game over")
      gameStarted = False
      snake.x = screenWidth / 2
      snake.y = screenHeight / 2
      gameOver = True

  # giving the screen its colour
  screen.fill(background)

  # pressing a button will turn one of the boolean values to true
  if not gameStarted:
    screen.fill(background)
    if startButton.draw(screen):
      gameStarted = True

  if gameStarted:
    # making the background and drawing the score, snake and fruit on top
    screen.fill(background)
    snake.draw(screen)
    print(snake.body[1], snake.body[2])
    apple.draw(screenWidth, screenHeight, screen)
    screen.blit(score, (0, 0))
    if apple.x - 17 <= snake.x <= apple.x + 17 and apple.y - 17 <= snake.y <= apple.y + 17:  # checking if the snake and fruit overlap
      apple.drawn = False
      snake.score += 1
      pygame.display.update()

  snake.move()
  pygame.display.update()
  # updating the screen

pygame.quit()